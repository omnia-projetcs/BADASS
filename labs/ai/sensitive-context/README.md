# Sensitive context

The context builder includes credentials in model-visible data.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-200 |
| OWASP | LLM02:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Send only allowlisted non-sensitive context fields.

## Regression

```sh
python3 tools/lab.py test --case ai/sensitive-context --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public context | benign | {"equals": {"question": "help"}} | {"equals": {"question": "help"}} |
| credential in context | attack | {"equals": {"question": "help", "api_key": "LAB_CANARY"}} | {"equals": {"question": "help"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
