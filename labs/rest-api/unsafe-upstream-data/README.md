# Unsafe upstream data

An upstream API value is accepted without validating business constraints.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-20  
**OWASP:** API10:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate type, bounds and schema of upstream responses.

## Regression

```sh
python3 tools/lab.py test --case rest-api/unsafe-upstream-data --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid upstream | benign | {"equals": 80} | {"equals": 80} |
| negative upstream | attack | {"equals": 1100} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
