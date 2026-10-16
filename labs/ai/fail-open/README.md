# Fail open

An authorization backend error grants access.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-636  
**OWASP:** A10:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Treat an indeterminate authorization result as denial.

## Regression

```sh
python3 tools/lab.py test --case ai/fail-open --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| authorized caller | benign | {"equals": "ALLOWED"} | {"equals": "ALLOWED"} |
| unauthorized caller | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| backend failure | attack | {"equals": "ALLOWED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
