# Symlink following

An export follows a preplaced symbolic link and overwrites a private file.

**Technology:** CGI (Python)  
**CWE:** CWE-59  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use atomic exclusive creation; reject an existing final path instead of following it. The parent directory is trusted.

## Regression

```sh
python3 tools/lab.py test --case cgi/symlink-following --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary export | benign | {"equals": "Content-Type: application/json\r\n\r\n\"LAB_SECRET\""} | {"equals": "Content-Type: application/json\r\n\r\n\"LAB_SECRET\""} |
| preplaced link | attack | {"equals": "Content-Type: application/json\r\n\r\n\"LAB_OVERWRITTEN\""} | {"equals": "Content-Type: application/json\r\n\r\n\"LAB_SECRET\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
