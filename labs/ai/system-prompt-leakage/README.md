# System prompt leakage

A debug API returns the internal system prompt to the client.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-200  
**OWASP:** LLM07:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep internal prompts out of client-visible diagnostics and never store secrets in prompts.

## Regression

```sh
python3 tools/lab.py test --case ai/system-prompt-leakage --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary status | benign | {"equals": "READY"} | {"equals": "READY"} |
| debug prompt | attack | {"equals": "LAB_INTERNAL_PROMPT"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
