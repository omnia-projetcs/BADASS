# Invalid purchase quantity

A negative purchase quantity increases the account balance.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-1284 |
| OWASP | A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Parse a complete decimal quantity and enforce 1 through 100 before calculating the price.

## Regression

```sh
python3 tools/lab.py test --case cpp/business-logic --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary order | benign | {"equals": "980"} | {"equals": "980"} |
| boundary order | benign | {"equals": "0"} | {"equals": "0"} |
| negative order | attack | {"equals": "1050"} | {"equals": "DENIED"} |
| zero order | attack | {"equals": "1000"} | {"equals": "DENIED"} |
| smallest order | benign | {"equals": "990"} | {"equals": "990"} |
| above order limit | attack | {"equals": "-10"} | {"equals": "DENIED"} |
| empty numeric input | robustness | {"stderr_contains": "stol", "exit_code": 1} | {"equals": "DENIED"} |
| nonnumeric input | robustness | {"stderr_contains": "stol", "exit_code": 1} | {"equals": "DENIED"} |
| trailing text | robustness | {"equals": "990"} | {"equals": "DENIED"} |
| fractional value | robustness | {"equals": "990"} | {"equals": "DENIED"} |
| exponent notation | robustness | {"equals": "990"} | {"equals": "DENIED"} |
| leading whitespace | robustness | {"equals": "990"} | {"equals": "DENIED"} |
| leading plus | robustness | {"equals": "990"} | {"equals": "DENIED"} |
| integer conversion overflow | robustness | {"stderr_contains": "stol", "exit_code": 1} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
