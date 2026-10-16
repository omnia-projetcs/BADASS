# Insecure direct object reference (IDOR)

A logged-in user retrieves another account by identifier.

**Technology:** Python  
**CWE:** CWE-639  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Check ownership against the authenticated server-side principal.

## Regression

```sh
python3 tools/lab.py test --case python/idor --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| own account | benign | {"equals": "ALICE_DATA"} | {"equals": "ALICE_DATA"} |
| other account | attack | {"equals": "BOB_PRIVATE"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
