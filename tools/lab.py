#!/usr/bin/env python3
"""BADASS command line: validation, regression, coverage and scanner scoring."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

from runner import ROOT, RUNTIMES, run_cases, valid_file_observation
from technology_coverage import build_matrix, validate_plan


def read_catalog():
    return json.loads((ROOT / "catalog/cases.json").read_text())


def read_plan():
    return json.loads((ROOT / "catalog/coverage-plan.json").read_text())


def validate(cases):
    seen = set()
    entries = json.loads((ROOT / "catalog/cwe.json").read_text())["entries"]
    validate_plan(read_plan(), entries, RUNTIMES)
    cwes = {x["id"] for x in entries if x["kind"] == "weakness"}
    frameworks = json.loads((ROOT / "catalog/frameworks.json").read_text())
    categories = {c for f in frameworks for c in f["categories"]}
    for case in cases:
        assert case["id"] not in seen, "Duplicate case: " + case["id"]
        seen.add(case["id"])
        assert case["language"] in RUNTIMES
        assert case.get("database") in {None, "sqlite"}, case["id"] + ": unsupported database"
        assert case["cwe"] and set(case["cwe"]) <= cwes, case["id"] + ": unknown CWE"
        assert set(case["owasp"]) <= categories, case["id"] + ": unknown OWASP category"
        assert case["description"] and case["remediation"] and case["scope"]
        if case.get("oracle"):
            assert case["language"] in {"python", "cgi", "rest-api", "ai"}
            assert re.fullmatch(r"[a-z][a-z0-9_]*", case["oracle"])
        for variant in ("vulnerable", "fixed"):
            path = (ROOT / case[variant]).resolve()
            assert path.is_relative_to(ROOT / "labs") and path.is_file(), str(path)
        assert case["vulnerable"] != case["fixed"]
        assert any(t["kind"] == "benign" for t in case["tests"]), case["id"]
        assert any(t["kind"] == "attack" and t["fixed"] != t["vulnerable"] for t in case["tests"]), case["id"]
        for t in case["tests"]:
            assert t["kind"] in {"benign", "attack", "functional", "robustness"}
            assert isinstance(t.get("context", {}), dict), case["id"] + ": invalid context"
            assert "context" not in t or case.get("oracle"), case["id"] + ": context requires an oracle"
            assert isinstance(t.get("env", {}), dict)
            assert all(re.fullmatch(r"BADASS_[A-Z0-9_]+", key) and isinstance(value, str)
                       and "\x00" not in value for key, value in t.get("env", {}).items())
            for variant in ("vulnerable", "fixed"):
                expected = t[variant]
                assert set(expected) <= {"equals", "stderr_contains", "exit_code", "files"}
                assert ("equals" in expected) != ("stderr_contains" in expected)
                if "stderr_contains" in expected:
                    assert isinstance(expected["stderr_contains"], str) and expected["stderr_contains"]
                if "exit_code" in expected:
                    assert type(expected["exit_code"]) is int and 0 <= expected["exit_code"] <= 255
                observations = expected.get("files", [])
                assert isinstance(observations, list), case["id"] + ": files must be an array"
                assert all(valid_file_observation(item) for item in observations), case["id"] + ": invalid file observation"
            if t["kind"] == "benign":
                assert t["fixed"] == t["vulnerable"], case["id"] + ": benign behavior differs"
    return len(cases)


def coverage(cases):
    taxonomy = json.loads((ROOT / "catalog/cwe.json").read_text())
    rows = []
    for entry in taxonomy["entries"]:
        ids = [c["id"] for c in cases if entry["id"] in c["cwe"]]
        status = "implemented" if ids else ("taxonomy-only" if entry["kind"] != "weakness" else "gap")
        rows.append({**entry, "coverage": status, "cases": ids})
    frameworks = json.loads((ROOT / "catalog/frameworks.json").read_text())
    owasp = {key: [c["id"] for c in cases if key in c["owasp"]] for f in frameworks for key in f["categories"]}
    return {"cwe_version": taxonomy["version"], "counts": dict(Counter(r["coverage"] for r in rows)),
            "note": "Implemented means source pair and vectors exist, not that a runtime passed or a scanner detected it.",
            "cwe": rows, "owasp": owasp,
            "by_technology": build_matrix(cases, taxonomy["entries"], read_plan())}


CWE_RE = re.compile(r"\bCWE-(\d+)\b", re.IGNORECASE)


def _extract_sarif_cwes(result, rules_by_id):
    cwes = []
    seen = set()

    def add_text(text):
        if not isinstance(text, str):
            return
        for match in CWE_RE.findall(text):
            cwe = f"CWE-{int(match)}"
            if cwe not in seen:
                seen.add(cwe)
                cwes.append(cwe)

    def scan_items(items):
        for item in items or ():
            if isinstance(item, dict):
                add_text(item.get("id"))
                target = item.get("target") or {}
                if isinstance(target, dict):
                    add_text(target.get("id"))
                    tool_comp = target.get("toolComponent") or {}
                    if isinstance(tool_comp, dict) and str(tool_comp.get("name", "")).upper() == "CWE":
                        add_text(target.get("id"))
            elif isinstance(item, str):
                add_text(item)

    rule_id = result.get("ruleId")
    rule = rules_by_id.get(rule_id, {}) if isinstance(rule_id, str) else {}
    scan_items(result.get("taxa"))
    scan_items(rule.get("relationships"))
    scan_items((result.get("properties") or {}).get("tags"))
    scan_items((rule.get("properties") or {}).get("tags"))
    if not cwes:
        add_text(rule_id)
        add_text((result.get("message") or {}).get("text"))
    return cwes


def parse_sarif(doc):
    """Convert a SARIF 2.1.0 report into finding dicts suitable for resolve_findings."""
    if not isinstance(doc, dict) or not isinstance(doc.get("runs"), list):
        raise ValueError("Expected a SARIF object with a runs array")
    findings = []
    for run in doc["runs"]:
        if not isinstance(run, dict):
            continue
        driver = ((run.get("tool") or {}).get("driver") or {})
        rules_by_id = {r["id"]: r for r in (driver.get("rules") or ()) if isinstance(r, dict) and r.get("id")}
        for result in run.get("results") or ():
            if not isinstance(result, dict):
                continue
            cwes = _extract_sarif_cwes(result, rules_by_id)
            locations = result.get("locations") or []
            uris = []
            for loc in locations:
                phys = (loc or {}).get("physicalLocation") or {}
                uri = ((phys.get("artifactLocation") or {}).get("uri"))
                if isinstance(uri, str) and uri:
                    uris.append(uri)
            if not uris:
                uris = [None]
            for uri in uris:
                for cwe in cwes or [None]:
                    item = {"cwe": cwe}
                    if uri:
                        if uri.startswith(("http://", "https://", "/t/")):
                            item["url"] = uri
                        else:
                            clean = uri[7:] if uri.startswith("file://") else uri
                            item["path"] = clean.lstrip("./") if clean.startswith("./") else clean
                    findings.append(item)
    return findings


def _target_id_from_url(raw):
    if not isinstance(raw, str) or not raw:
        return None
    path = urlsplit(raw).path
    if path.startswith("/t/"):
        return path[3:].strip("/")
    return None


def resolve_findings(findings, mapping=None, cases=None):
    """Resolve opaque blind paths, target URLs, or repo paths to (case_id, variant, cwe)."""
    if not isinstance(findings, list):
        raise ValueError("Expected a findings list")
    targets = (mapping or {}).get("targets") or {}
    files = (mapping or {}).get("files") or {}
    services = (mapping or {}).get("services") or {}
    case_dirs = {}
    for c in cases or ():
        for v in ("vulnerable", "fixed"):
            parent = str(Path(c[v]).parent).replace("\\", "/")
            case_dirs[parent] = (c["id"], v)
    named_cases = {c["id"] for c in (cases or ())}

    resolved = []
    for f in findings:
        if not isinstance(f, dict):
            resolved.append(f)
            continue
        if f.get("case_id") and f.get("variant"):
            resolved.append(f)
            continue
        out = dict(f)
        tid = f.get("target_id") or _target_id_from_url(f.get("url")) or _target_id_from_url(f.get("path"))
        if tid and tid in targets:
            out["case_id"] = targets[tid]["case_id"]
            out["variant"] = targets[tid]["variant"]
        elif tid and tid.count("/") >= 2:
            parts = tid.rsplit("/", 1)
            if parts[1] in {"vulnerable", "fixed"} and (not named_cases or parts[0] in named_cases):
                out["case_id"] = parts[0]
                out["variant"] = parts[1]
        elif f.get("port") is not None and services:
            key = f"{f.get('service', '')}:{f['port']}" if f.get("service") else None
            entry = services.get(key) if key else next(
                (v for v in services.values() if v.get("port") == f["port"]), None
            )
            if entry:
                out["case_id"] = entry["case_id"]
                out["variant"] = entry["variant"]
        elif isinstance(f.get("path"), str):
            norm_path = f["path"].replace("\\", "/").lstrip("./")
            if norm_path in targets:
                out["case_id"] = targets[norm_path]["case_id"]
                out["variant"] = targets[norm_path]["variant"]
            elif norm_path in files:
                out["case_id"] = files[norm_path]["case_id"]
                out["variant"] = files[norm_path]["variant"]
            else:
                matched = next(
                    (meta for rel, meta in files.items() if norm_path.endswith("/" + rel)),
                    None,
                )
                if matched:
                    out["case_id"] = matched["case_id"]
                    out["variant"] = matched["variant"]
                else:
                    for prefix, (cid, var) in case_dirs.items():
                        if norm_path == prefix or norm_path.startswith(prefix + "/") or ("/" + prefix + "/") in norm_path:
                            out["case_id"] = cid
                            out["variant"] = var
                            break
        resolved.append(out)
    return resolved


def score(cases, findings):
    """Exact case + variant + CWE matching; fixed examples are negative controls."""
    known = {c["id"]: c for c in cases}
    expected = {(c["id"], w) for c in cases for w in c["cwe"]}
    tp, fp, detected, unknown = set(), set(), set(), []
    for f in findings:
        cid, variant, cwe = f.get("case_id"), f.get("variant"), f.get("cwe")
        if cid not in known or variant not in {"fixed", "vulnerable"} or not isinstance(cwe, str):
            unknown.append(f)
            continue
        key = (cid, cwe)
        if variant == "vulnerable" and key in expected:
            tp.add(key)
            detected.add(cid)
        else:
            fp.add((cid, variant, cwe))
    fn = expected - tp
    return {"true_positives": len(tp), "false_positives": len(fp), "false_negatives": len(fn),
            "precision": len(tp) / (len(tp) + len(fp)) if tp or fp else None,
            "recall": len(tp) / len(expected) if expected else None,
            "detected_cases": len(detected), "total_cases": len(cases), "unknown_findings": unknown,
            "missed": [{"case_id": c, "cwe": w} for c, w in sorted(fn)],
            "note": "Scoring only the declared target weaknesses. Other valid findings require manual triage."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "validate", "test", "coverage", "score"])
    parser.add_argument("--language", choices=sorted(RUNTIMES))
    parser.add_argument("--case")
    parser.add_argument("--cwe", help="Select cases for a weakness, for example CWE-89")
    parser.add_argument("--strict", action="store_true", help="Fail when a runtime is missing")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--findings", type=Path)
    parser.add_argument("--sarif", type=Path, help="SARIF 2.1.0 report to score")
    parser.add_argument("--mapping", type=Path, help="Blind mapping JSON from export_blind.py or netserve.py")
    args = parser.parse_args()
    cases = read_catalog()
    validate(cases)
    cases = [c for c in cases if (not args.language or c["language"] == args.language)
             and (not args.case or c["id"] == args.case) and (not args.cwe or args.cwe in c["cwe"])]
    if not cases:
        parser.error("No matching cases")
    failed = False
    if args.command == "validate":
        result = {"valid_cases": len(cases)}
    elif args.command == "list":
        result = [{k: c[k] for k in ("id", "language", "cwe", "owasp", "scope")} for c in cases]
    elif args.command == "coverage":
        result = coverage(cases)
    elif args.command == "score":
        if not args.findings and not args.sarif:
            parser.error("score requires --findings or --sarif")
        mapping = json.loads(args.mapping.read_text()) if args.mapping else None
        if args.sarif:
            raw_findings = parse_sarif(json.loads(args.sarif.read_text()))
        else:
            raw = json.loads(args.findings.read_text())
            raw_findings = parse_sarif(raw) if isinstance(raw, dict) and "runs" in raw else raw
        resolved = resolve_findings(raw_findings, mapping=mapping, cases=cases)
        result = score(cases, resolved)
        failed = bool(result["unknown_findings"])
    else:
        records, failed = run_cases(cases, args.strict)
        result = {"created_at": datetime.now(timezone.utc).isoformat(),
                  "summary": dict(Counter(r["status"] for r in records)), "results": records}
    serialized = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
        print("Report:", args.output)
        if "summary" in result:
            print(json.dumps(result["summary"]))
    else:
        print(serialized)
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
