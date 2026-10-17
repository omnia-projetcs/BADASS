# Function authorization

A normal authenticated user invokes an administrative function.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-862 |
| OWASP | API5:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Authorize functions using a trusted server-side role.

## Regression

```sh
python3 tools/lab.py test --case rest-api/function-authorization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public health | benign | {"equals": "HEALTHY"} | {"equals": "HEALTHY"} |
| admin function | attack | {"equals": "ALL_USERS_DELETED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
