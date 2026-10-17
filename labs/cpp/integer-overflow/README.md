# Integer overflow

Unsigned multiplication wraps and undercharges an order.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-190 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Require a complete unsigned 32-bit decimal quantity, reject signed or overflowing conversions, and check the multiplication bound before computing the total.

## Regression

```sh
python3 tools/lab.py test --case cpp/integer-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal order | benign | {"equals": "100"} | {"equals": "100"} |
| largest safe quantity | benign | {"equals": "4294967200"} | {"equals": "4294967200"} |
| wrapping order | attack | {"equals": "4"} | {"equals": "DENIED"} |
| zero quantity | benign | {"equals": "0"} | {"equals": "0"} |
| second wrapping quantity | attack | {"equals": "104"} | {"equals": "DENIED"} |
| maximum uint32 quantity | attack | {"equals": "4294967196"} | {"equals": "DENIED"} |
| empty quantity | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| nonnumeric quantity | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| trailing quantity text | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| fractional quantity | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| negative quantity | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| quantity above uint32 | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| quantity above uint64 | robustness | {"equals": "", "exit_code": 2} | {"equals": "DENIED"} |
| negative zero | robustness | {"equals": "0"} | {"equals": "DENIED"} |
| wrapped negative conversion | robustness | {"equals": "100"} | {"equals": "DENIED"} |
| leading whitespace | robustness | {"equals": "100"} | {"equals": "DENIED"} |
| leading plus | robustness | {"equals": "100"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
