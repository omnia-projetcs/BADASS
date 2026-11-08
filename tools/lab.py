#!/usr/bin/env python3
"""BADASS command line: validation, regression, coverage and scanner scoring."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys

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
        if not args.findings:
            parser.error("score requires --findings")
        result = score(cases, json.loads(args.findings.read_text()))
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
