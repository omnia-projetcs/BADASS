"""An argv list avoids a shell but still lets input become a child-tool option."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def search_tool(arguments):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--include-private", action="store_true")
    parser.add_argument("query", nargs="?", default="")
    options = parser.parse_args(arguments)
    records = ["PUBLIC_REPORT", "PUBLIC_NOTES"]
    if options.include_private:
        records.append("LAB_PRIVATE_REPORT")
    print(json.dumps([record for record in records if options.query.lower() in record.lower()]))


def run(query):
    if not isinstance(query, str) or len(query) > 128 or "\x00" in query:
        return {"status": 400, "error": "invalid query"}
    try:
        query.encode("utf-8")
    except UnicodeEncodeError:
        return {"status": 400, "error": "invalid query"}
    # VULNERABLE: the child interprets a leading --include-private as an option.
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", query]
    result = subprocess.run(command, shell=False, capture_output=True, text=True, timeout=3)
    if result.returncode != 0:
        return {"status": 400, "error": "invalid tool argument"}
    try:
        return {"status": 200, "matches": json.loads(result.stdout)}
    except json.JSONDecodeError:
        return {"status": 400, "error": "invalid tool argument"}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "--worker":
        raise SystemExit("Use the BADASS runner")
    search_tool(sys.argv[2:])
