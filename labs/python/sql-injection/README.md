# SQL injection

Concatenated SQL exposes another account.

**Technology:** Python  
**CWE:** CWE-89  
**OWASP:** A05:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Bind parameters instead of interpolating SQL.

## Regression

```sh
python3 tools/lab.py test --case python/sql-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| existing account | benign | {"equals": ["alice"]} | {"equals": ["alice"]} |
| SQL predicate | attack | {"equals": ["alice", "admin"]} | {"equals": []} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
