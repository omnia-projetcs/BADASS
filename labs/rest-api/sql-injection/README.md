# SQL injection

A JSON API field is concatenated into SQL and bypasses the account lookup predicate.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-89 |
| OWASP | A05:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep SQL structure constant and bind the untrusted value as a parameter. Execute against a fresh in-memory SQLite database.

## Regression

```sh
python3 tools/lab.py test --case rest-api/sql-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| existing account | benign | {"equals": {"status": 200, "body": ["alice"]}} | {"equals": {"status": 200, "body": ["alice"]}} |
| missing account | benign | {"equals": {"status": 200, "body": []}} | {"equals": {"status": 200, "body": []}} |
| empty value | benign | {"equals": {"status": 200, "body": []}} | {"equals": {"status": 200, "body": []}} |
| ordinary SQL-looking text | benign | {"equals": {"status": 200, "body": []}} | {"equals": {"status": 200, "body": []}} |
| tautology with comment | attack | {"equals": {"status": 200, "body": ["alice", "admin"]}} | {"equals": {"status": 200, "body": []}} |
| targeted account bypass | attack | {"equals": {"status": 200, "body": ["admin"]}} | {"equals": {"status": 200, "body": []}} |
| UNION injected row | attack | {"equals": {"status": 200, "body": ["LAB_UNION"]}} | {"equals": {"status": 200, "body": []}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
