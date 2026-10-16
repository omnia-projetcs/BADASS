# Unbounded work

A client controls the amount of allocation and processing.

**Technology:** Python  
**CWE:** CWE-400  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce input and work budgets before allocating or iterating.

## Regression

```sh
python3 tools/lab.py test --case python/unbounded-work --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| small request | benign | {"equals": 10} | {"equals": 10} |
| exceeds budget | attack | {"equals": 101} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
