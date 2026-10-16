# Error disclosure

A failed database operation returns internal credentials to the client.

**Technology:** Python  
**CWE:** CWE-209  
**OWASP:** A02:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Return a generic failure and keep appropriately redacted diagnostics server-side.

## Regression

```sh
python3 tools/lab.py test --case python/error-disclosure --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| success | benign | {"equals": "OK"} | {"equals": "OK"} |
| error details | attack | {"equals": "db://admin:LAB_SECRET@database/internal"} | {"equals": "Service unavailable"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
