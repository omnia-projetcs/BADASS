# Training data poisoning

Unreviewed labels overwrite a curated security training record.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-20  
**OWASP:** LLM04:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Preserve reviewed labels and quarantine untrusted submissions.

## Regression

```sh
python3 tools/lab.py test --case ai/training-data-poisoning --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| unrelated submission | benign | {"equals": "vulnerable"} | {"equals": "vulnerable"} |
| poisoned label | attack | {"equals": "safe"} | {"equals": "vulnerable"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
