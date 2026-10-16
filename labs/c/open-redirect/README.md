# Open redirect

A client-selected destination produces an external redirect.

**Technology:** C  
**CWE:** CWE-601  
**OWASP:** A01:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Allowlist complete application-local destinations, including rejection of scheme-relative URLs.

## Regression

```sh
python3 tools/lab.py test --case c/open-redirect --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| local home | benign | {"equals": "Location: /home"} | {"equals": "Location: /home"} |
| local profile | benign | {"equals": "Location: /profile"} | {"equals": "Location: /profile"} |
| external destination | attack | {"equals": "Location: https://attacker.invalid"} | {"equals": "DENIED"} |
| scheme-relative destination | attack | {"equals": "Location: //attacker.invalid"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
