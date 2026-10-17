# Excessive agency

The tool gateway authorizes writes solely because the model requested them.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-862 |
| OWASP | LLM06:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce task-scoped capabilities independently of model output.

## Regression

```sh
python3 tools/lab.py test --case ai/excessive-agency --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| authorized tool | benign | {"equals": "EXECUTED:read_source"} | {"equals": "EXECUTED:read_source"} |
| unauthorized patch | attack | {"equals": "EXECUTED:write_file"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
