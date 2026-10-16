# Model artifact integrity

A model artifact is accepted after untrusted replacement.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-494  
**OWASP:** LLM03:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Verify a digest from a separately trusted model registry.

## Regression

```sh
python3 tools/lab.py test --case ai/model-artifact-integrity --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| approved artifact | benign | {"equals": "approved-model"} | {"equals": "approved-model"} |
| substituted artifact | attack | {"equals": "poisoned-model"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
