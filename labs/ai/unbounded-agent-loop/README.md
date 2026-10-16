# Unbounded agent loop

A model controls the number of tool-loop iterations.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-834  
**OWASP:** LLM10:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Set a hard server-side iteration budget independently of model requests.

## Regression

```sh
python3 tools/lab.py test --case ai/unbounded-agent-loop --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| bounded plan | benign | {"equals": 3} | {"equals": 3} |
| over-budget plan | attack | {"equals": 6} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
