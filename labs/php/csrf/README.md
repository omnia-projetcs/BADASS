# Cross-site request forgery (CSRF)

A PHP state-changing transfer handler executes requests without checking the session anti-CSRF token.

| Attribute | Value |
|---|---|
| Technology | PHP |
| CWE | CWE-352 |
| OWASP | A01:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.php) · [Corrected source](fixed/main.php)

## Correction

Require a string csrf token in the request and verify it against the session token using hash_equals().

## Regression

```sh
python3 tools/lab.py test --case php/csrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid CSRF token | benign | {"equals": "TRANSFERRED"} | {"equals": "TRANSFERRED"} |
| missing CSRF token | attack | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
