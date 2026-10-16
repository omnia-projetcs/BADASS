# Predictable token

Reset tokens are derived from public account names.

**Technology:** Python  
**CWE:** CWE-330  
**OWASP:** A07:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Generate unpredictable tokens with a cryptographic random generator.

## Regression

```sh
python3 tools/lab.py test --case python/predictable-token --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty account | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| predictable reset | attack | {"equals": true} | {"equals": false} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
