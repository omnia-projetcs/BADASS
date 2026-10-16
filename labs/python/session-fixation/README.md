# Session fixation

Login upgrades a client-selected session identifier.

**Technology:** Python  
**CWE:** CWE-384  
**OWASP:** A07:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Invalidate the pre-login session and issue a fresh random identifier.

## Regression

```sh
python3 tools/lab.py test --case python/session-fixation --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| unrelated session | benign | {"equals": false} | {"equals": false} |
| fixed session id | attack | {"equals": true} | {"equals": false} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
