# Unbounded work

A client controls memory allocation without an application budget.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-400 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Parse a complete nonnegative decimal size and enforce the limit before allocating memory.

## Regression

```sh
python3 tools/lab.py test --case cpp/unbounded-work --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| small allocation | benign | {"equals": "10"} | {"equals": "10"} |
| limit boundary | benign | {"equals": "100"} | {"equals": "100"} |
| over budget | attack | {"equals": "101"} | {"equals": "DENIED"} |
| large request | attack | {"equals": "1000"} | {"equals": "DENIED"} |
| empty allocation | benign | {"equals": "0"} | {"equals": "0"} |
| negative allocation | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| empty numeric input | robustness | {"stderr_contains": "stoi", "exit_code": 1} | {"equals": "DENIED"} |
| nonnumeric input | robustness | {"stderr_contains": "stoi", "exit_code": 1} | {"equals": "DENIED"} |
| trailing text | robustness | {"equals": "1"} | {"equals": "DENIED"} |
| fractional value | robustness | {"equals": "1"} | {"equals": "DENIED"} |
| exponent notation | robustness | {"equals": "1"} | {"equals": "DENIED"} |
| leading whitespace | robustness | {"equals": "1"} | {"equals": "DENIED"} |
| leading plus | robustness | {"equals": "1"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
