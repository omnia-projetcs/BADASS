# Business flow abuse

Repeated reservations bypass a per-account purchase limit.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-799  
**OWASP:** API6:2023  
**Test scope:** `state-machine-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce the quota in trusted persistent state atomically.

## Regression

```sh
python3 tools/lab.py test --case rest-api/business-flow-abuse --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| one reservation | benign | {"equals": 1} | {"equals": 1} |
| quota abuse | attack | {"equals": 3} | {"equals": 2} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
