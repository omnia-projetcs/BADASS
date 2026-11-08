#!/usr/bin/env python3
"""Run a nonempty, fail-closed smoke gate using only the Python standard library."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from lab import read_catalog, validate
from runner import run_cases

SMOKE_IDS = {
    "python/sql-injection", "python/predictable-token", "python/weak-password-hash",
    "python/session-fixation", "rest-api/unsafe-upstream-data", "ai/unverified-security-claim",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("reports/smoke.json"))
    args = parser.parse_args()
    cases = read_catalog()
    validate(cases)
    selected = [case for case in cases if case["id"] in SMOKE_IDS]
    if {case["id"] for case in selected} != SMOKE_IDS:
        raise RuntimeError("Required smoke cases are missing")
    records, failed = run_cases(selected, strict=True)
    checks = sum(len(record.get("checks", [])) for record in records)
    failed = failed or checks == 0 or len(records) != len(SMOKE_IDS)
    report = {"created_at": datetime.now(timezone.utc).isoformat(), "checks": checks,
              "summary": dict(Counter(record["status"] for record in records)), "results": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"checks": checks, "summary": report["summary"]}))
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
