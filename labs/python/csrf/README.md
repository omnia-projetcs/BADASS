# Cross-site request forgery (CSRF)

An authenticated state change ignores the anti-CSRF token.

**Technology:** Python  
**CWE:** CWE-352  
**OWASP:** A01:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require a token bound to the authenticated session and compare it safely.

## Regression

```sh
python3 tools/lab.py test --case python/csrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid token | benign | {"equals": "TRANSFERRED"} | {"equals": "TRANSFERRED"} |
| missing token | attack | {"equals": "TRANSFERRED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
