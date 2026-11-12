# User enumeration

The authentication handler returns distinct status codes and error messages for non-existent users versus wrong passwords, enabling account enumeration.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-203, CWE-208 |
| OWASP | A07:2025, API2:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Perform dummy key derivation when an account is absent, compare digests in constant time, and return an identical generic authentication failure.

## Regression

```sh
python3 tools/lab.py test --case rest-api/user-enumeration --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid login | benign | {"equals": {"status": 200, "user": "alice"}} | {"equals": {"status": 200, "user": "alice"}} |
| unknown account probe | attack | {"equals": {"status": 404, "error": "USER_NOT_FOUND"}} | {"equals": {"status": 401, "error": "INVALID_CREDENTIALS"}} |
| known account wrong password | attack | {"equals": {"status": 401, "error": "WRONG_PASSWORD"}} | {"equals": {"status": 401, "error": "INVALID_CREDENTIALS"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
