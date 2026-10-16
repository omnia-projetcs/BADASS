# Unbounded work

A client controls memory allocation without an application budget.

**Technology:** TypeScript  
**CWE:** CWE-400  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.ts) · [Corrected source](fixed/main.ts)

## Correction

Validate the requested size and enforce a limit before allocating.

## Regression

```sh
python3 tools/lab.py test --case typescript/unbounded-work --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| small allocation | benign | {"equals": "10"} | {"equals": "10"} |
| limit boundary | benign | {"equals": "100"} | {"equals": "100"} |
| over budget | attack | {"equals": "101"} | {"equals": "DENIED"} |
| large request | attack | {"equals": "1000"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
