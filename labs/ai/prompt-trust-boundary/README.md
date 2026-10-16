# Prompt trust boundary

Retrieved instructions can become privileged chat messages.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-1427  
**OWASP:** LLM01:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep external content in an untrusted data message; enforce tool permissions outside the model.

## Regression

```sh
python3 tools/lab.py test --case ai/prompt-trust-boundary --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary document | benign | {"equals": ["system", "user"]} | {"equals": ["system", "user"]} |
| role spoofing | attack | {"equals": ["system", "system"]} | {"equals": ["system", "user"]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
