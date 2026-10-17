# Cross-site request forgery (CSRF)

An authenticated state change ignores the anti-CSRF token.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-352 |
| OWASP | A01:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require the synthetic server-side session token, validate the request and ASCII token types, and compare safely. Non-ASCII strings and invalid JSON types are rejected without an exception.

## Regression

```sh
python3 tools/lab.py test --case python/csrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid token | benign | {"equals": "TRANSFERRED"} | {"equals": "TRANSFERRED"} |
| missing token | attack | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |
| wrong token | attack | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |
| non-ASCII token | robustness | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |
| null token | robustness | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |
| structured token | robustness | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |
| non-object request | robustness | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
