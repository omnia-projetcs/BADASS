# Hardcoded credentials

An embedded maintenance password grants access.

**Technology:** Python  
**CWE:** CWE-798  
**OWASP:** A07:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Remove embedded credentials and validate against the configured identity provider.

## Regression

```sh
python3 tools/lab.py test --case python/hardcoded-credentials --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| invalid password | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| embedded password | attack | {"equals": "ADMIN"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
