# Error disclosure

A failed file-backed service returns internal connection credentials.

| Attribute | Value |
|---|---|
| Technology | TypeScript |
| CWE | CWE-209 |
| OWASP | A02:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.ts) · [Corrected source](fixed/main.ts)

## Correction

Return a generic error without exposing internal configuration.

## Regression

```sh
python3 tools/lab.py test --case typescript/error-disclosure --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| healthy service | benign | {"equals": "OK"} | {"equals": "OK"} |
| service failure | attack | {"equals": "db://admin:LAB_SECRET@database/internal"} | {"equals": "Service unavailable"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
