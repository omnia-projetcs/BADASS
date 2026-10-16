# SQL injection

A decoded CGI query parameter changes an executed SQL query and leaks account rows.

**Technology:** CGI (Python)  
**CWE:** CWE-89  
**OWASP:** A05:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep SQL structure constant and bind the untrusted value as a parameter. Execute against a fresh in-memory SQLite database.

## Regression

```sh
python3 tools/lab.py test --case cgi/sql-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| existing account | benign | {"equals": "Content-Type: application/json\r\n\r\n[\"alice\"]"} | {"equals": "Content-Type: application/json\r\n\r\n[\"alice\"]"} |
| missing account | benign | {"equals": "Content-Type: application/json\r\n\r\n[]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |
| empty value | benign | {"equals": "Content-Type: application/json\r\n\r\n[]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |
| ordinary SQL-looking text | benign | {"equals": "Content-Type: application/json\r\n\r\n[]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |
| tautology with comment | attack | {"equals": "Content-Type: application/json\r\n\r\n[\"alice\", \"admin\"]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |
| targeted account bypass | attack | {"equals": "Content-Type: application/json\r\n\r\n[\"admin\"]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |
| UNION injected row | attack | {"equals": "Content-Type: application/json\r\n\r\n[\"LAB_UNION\"]"} | {"equals": "Content-Type: application/json\r\n\r\n[]"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
