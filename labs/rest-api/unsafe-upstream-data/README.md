# Unsafe upstream data

An upstream API value is accepted without validating business constraints.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-20 |
| OWASP | API10:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the request object and nested upstream object before reading the price; require an exact integer in [0,100]. Missing data, nulls, arrays, strings, booleans and fractions are rejected cleanly.

## Regression

```sh
python3 tools/lab.py test --case rest-api/unsafe-upstream-data --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid upstream | benign | {"equals": 80} | {"equals": 80} |
| negative upstream | attack | {"equals": 1100} | {"equals": "DENIED"} |
| minimum valid price | benign | {"equals": 100} | {"equals": 100} |
| maximum valid price | benign | {"equals": 0} | {"equals": 0} |
| price over upper bound | attack | {"equals": -1} | {"equals": "DENIED"} |
| boolean is not a price | robustness | {"equals": 99} | {"equals": "DENIED"} |
| fractional price | robustness | {"equals": 79.5} | {"equals": "DENIED"} |
| null upstream | robustness | {"stderr_contains": "TypeError"} | {"equals": "DENIED"} |
| list upstream | robustness | {"stderr_contains": "TypeError"} | {"equals": "DENIED"} |
| string upstream | robustness | {"stderr_contains": "TypeError"} | {"equals": "DENIED"} |
| missing price | robustness | {"stderr_contains": "KeyError"} | {"equals": "DENIED"} |
| missing upstream | robustness | {"stderr_contains": "KeyError"} | {"equals": "DENIED"} |
| non-object request | robustness | {"stderr_contains": "TypeError"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
