# Error disclosure

A failed file-backed service returns internal connection credentials.

**Technology:** C++  
**CWE:** CWE-209  
**OWASP:** A02:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Return a generic error without exposing internal configuration.

## Regression

```sh
python3 tools/lab.py test --case cpp/error-disclosure --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| healthy service | benign | {"equals": "OK"} | {"equals": "OK"} |
| service failure | attack | {"equals": "db://admin:LAB_SECRET@database/internal"} | {"equals": "Service unavailable"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
