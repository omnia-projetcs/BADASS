# File create race

A writer checks that report.txt does not exist, then opens it for writing. A synchronized attacker thread inserts a symlink in that interval, redirecting the write to a synthetic victim file. EDB-24749 motivates insecure temporary-file symlink attacks; the deterministic check/use schedule is an original extension.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-367 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use exclusive atomic file creation (open mode x) so a file or symlink appearing after the check causes a conflict instead of an overwrite. The parent directory is fixed and trusted; only the final filename is raced. Event synchronization makes the attack deterministic without timing thresholds. The fixture runs only in its owned workspace and never touches real system temporary files.

## Regression

```sh
python3 tools/lab.py test --case python/file-create-race --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary report | benign | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": "LAB_REPORT"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": "LAB_REPORT"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} |
| Unicode report | benign | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": "Résumé\n"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": "Résumé\n"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} |
| empty report | benign | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": ""}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} | {"equals": {"status": 201}, "files": [{"path": "report.txt", "content": ""}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} |
| symlink insertion overwrites victim | attack | {"equals": {"status": 201}, "files": [{"path": "report.txt", "type": "symlink", "target": "victim.txt"}, {"path": "victim.txt", "content": "LAB_OVERWRITTEN"}]} | {"equals": {"status": 409}, "files": [{"path": "report.txt", "type": "symlink", "target": "victim.txt"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} |
| symlink insertion can truncate victim | attack | {"equals": {"status": 201}, "files": [{"path": "report.txt", "type": "symlink", "target": "victim.txt"}, {"path": "victim.txt", "content": ""}]} | {"equals": {"status": 409}, "files": [{"path": "report.txt", "type": "symlink", "target": "victim.txt"}, {"path": "victim.txt", "content": "LAB_ORIGINAL"}]} |
| non-object request | robustness | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} |
| missing schedule | robustness | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} |
| non-boolean schedule | robustness | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} |
| non-string content | robustness | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} |
| oversized content | robustness | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "report.txt", "type": "absent"}, {"path": "victim.txt", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-367 — Time-of-check Time-of-use Race Condition](https://cwe.mitre.org/data/definitions/367.html)
- [EDB-24749 — Cscope insecure temporary file creation — Gangstuck / Psirac](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/linux/local/24749.sh)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
