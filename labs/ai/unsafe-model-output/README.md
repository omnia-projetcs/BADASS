# Unsafe model output

Generated model output is inserted into HTML without encoding.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-79  
**OWASP:** LLM05:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Treat generated output as untrusted and encode for its destination context.

## Regression

```sh
python3 tools/lab.py test --case ai/unsafe-model-output --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain answer | benign | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} |
| generated markup | attack | {"equals": "&lt;p&gt;&lt;script&gt;alert(1)&lt;/script&gt;&lt;/p&gt;"} | {"equals": "&lt;p&gt;&amp;lt;script&amp;gt;alert(1)&amp;lt;/script&amp;gt;&lt;/p&gt;"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
