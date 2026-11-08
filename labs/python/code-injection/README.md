# Code injection

A calculator evaluates arbitrary Python expressions.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-95 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Accept only a bounded arithmetic grammar and never call eval.

## Regression

```sh
python3 tools/lab.py test --case python/code-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| addition | benign | {"equals": 5} | {"equals": 5} |
| file read | attack | {"equals": "LAB_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
