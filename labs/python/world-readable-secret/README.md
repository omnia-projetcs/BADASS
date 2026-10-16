# World readable secret

A secret file is accessible to other local users.

**Technology:** Python  
**CWE:** CWE-732  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Set owner-only permissions before storing sensitive bytes.

## Regression

```sh
python3 tools/lab.py test --case python/world-readable-secret --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| no operation | benign | {"equals": "IGNORED"} | {"equals": "IGNORED"} |
| permission exposure | attack | {"equals": "0o644"} | {"equals": "0o600"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
