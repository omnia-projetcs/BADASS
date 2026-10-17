# Format string

User input is interpreted as a printf format string.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-134 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Always use a constant format string.

## Regression

```sh
python3 tools/lab.py test --case cpp/format-string --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| literal text | benign | {"equals": "hello"} | {"equals": "hello"} |
| format directive | attack | {"equals": "value=2a"} | {"equals": "value=%x"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
