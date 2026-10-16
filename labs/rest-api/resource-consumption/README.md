# Resource consumption

An API allocates a client-selected number of result rows.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-770  
**OWASP:** API4:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Cap page size before allocating memory.

## Regression

```sh
python3 tools/lab.py test --case rest-api/resource-consumption --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| small page | benign | {"equals": 10} | {"equals": 10} |
| oversized page | attack | {"equals": 101} | {"equals": {"status": 400}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
