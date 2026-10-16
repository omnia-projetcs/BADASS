"""Exact CWE-by-technology accounting; unreviewed applicability is never N/A."""
from collections import Counter, defaultdict


def validate_plan(plan, entries, languages):
    weaknesses = {e["id"] for e in entries if e["kind"] == "weakness"}
    assert set(plan["technologies"]) == set(languages), "Coverage plan must name every runtime"
    assert len(plan["technologies"]) == len(languages), "Duplicate technology"
    assert plan["scope"].strip(), "Coverage scope is required"
    seen = set()
    for group in plan["groups"]:
        assert group["id"] not in seen, "Duplicate coverage group"
        seen.add(group["id"])
        assert group["scope"].strip(), "Group scope is required"
        assert group["technologies"] and set(group["technologies"]) <= set(languages)
        assert len(group["technologies"]) == len(set(group["technologies"]))
        assert group["cwe"] and set(group["cwe"]) <= weaknesses, "Unknown target CWE"
        assert len(group["cwe"]) == len(set(group["cwe"])), "Duplicate target CWE"
    return plan


def build_matrix(cases, entries, plan):
    """A case in one technology cannot fill a different technology's cell."""
    languages = plan["technologies"]
    validate_plan(plan, entries, languages)
    targets = {(w, lang) for group in plan["groups"]
               for w in group["cwe"] for lang in group["technologies"]}
    evidence = defaultdict(list)
    for case in cases:
        for weakness in case["cwe"]:
            evidence[weakness, case["language"]].append(case["id"])
    rows = []
    for entry in entries:
        if entry["kind"] != "weakness":
            continue
        cells = {}
        for language in languages:
            key = (entry["id"], language)
            ids = sorted(set(evidence[key]))
            status = "implemented" if ids else ("gap" if key in targets else "unassessed")
            cells[language] = {"status": status, "targeted": key in targets, "cases": ids}
        rows.append({"id": entry["id"], "name": entry["name"],
                     "mitre_status": entry["status"], "technologies": cells})
    summary = {}
    for language in languages:
        counts = Counter(row["technologies"][language]["status"] for row in rows)
        summary[language] = {
            "cases": sum(c["language"] == language for c in cases),
            **{s: counts[s] for s in ("implemented", "gap", "unassessed")},
            "targets": sum(lang == language for _, lang in targets),
            "targets_implemented": sum(bool(evidence[w, lang]) for w, lang in targets if lang == language),
        }
    return {"technologies": languages, "scope": plan["scope"], "summary": summary, "rows": rows,
            "note": "Exact CWE mappings only. Implemented is source/vector evidence, not execution evidence. "
                    "Gap is a planned but absent case; unassessed means no case and applicability not reviewed. "
                    "Neither absence status means not applicable. Filters restrict case evidence."}
