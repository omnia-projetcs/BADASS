# Open redirect

An arbitrary post-login URL redirects users to an external site.

**Technology:** Python  
**CWE:** CWE-601  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use a fixed allowlist of application destinations.

## Regression

```sh
python3 tools/lab.py test --case python/open-redirect --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| local path | benign | {"equals": "Location: /home"} | {"equals": "Location: /home"} |
| external URL | attack | {"equals": "Location: https://attacker.invalid"} | {"equals": "DENIED"} |
| scheme-relative URL | attack | {"equals": "Location: //attacker.invalid"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
