# Legacy endpoint

An undocumented legacy debug endpoint still exposes account data.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-489  
**OWASP:** API9:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Remove retired routes and maintain an explicit route inventory.

## Regression

```sh
python3 tools/lab.py test --case rest-api/legacy-endpoint --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| current endpoint | benign | {"equals": "OK"} | {"equals": "OK"} |
| retired debug route | attack | {"equals": "LAB_PRIVATE_USERS"} | {"equals": "NOT_FOUND"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
