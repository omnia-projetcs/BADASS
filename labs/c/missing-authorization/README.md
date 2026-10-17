# Missing authorization

A normal authenticated user can invoke an administrative operation.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-862 |
| OWASP | A01:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Authorize the operation using the server-side role before changing state.

## Regression

```sh
python3 tools/lab.py test --case c/missing-authorization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public health | benign | {"equals": "HEALTHY"} | {"equals": "HEALTHY"} |
| admin operation | attack | {"equals": "USERS_DELETED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
