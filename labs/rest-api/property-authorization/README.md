# Property authorization

Profile updates allow callers to change protected fields.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-915  
**OWASP:** API3:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Update only explicitly writable properties.

## Regression

```sh
python3 tools/lab.py test --case rest-api/property-authorization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| display name | benign | {"equals": {"display_name": "A", "role": "user"}} | {"equals": {"display_name": "A", "role": "user"}} |
| privileged field | attack | {"equals": {"display_name": "Alice", "role": "admin"}} | {"equals": {"display_name": "Alice", "role": "user"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
