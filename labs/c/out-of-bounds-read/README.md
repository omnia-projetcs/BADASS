# Out of bounds read

An unchecked index reads beyond a stack array.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-125 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Parse a complete in-range decimal integer, then validate both lower and upper array bounds before access.

## Regression

```sh
python3 tools/lab.py test --case c/out-of-bounds-read --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid index | benign | {"equals": "20"} | {"equals": "20"} |
| out of bounds | attack | {"stderr_contains": "stack-buffer-overflow"} | {"equals": "DENIED"} |
| first element | benign | {"equals": "10"} | {"equals": "10"} |
| last element | benign | {"equals": "30"} | {"equals": "30"} |
| first out-of-range index | attack | {"stderr_contains": "stack-buffer-overflow"} | {"equals": "DENIED"} |
| negative index | attack | {"stderr_contains": "index -1 out of bounds for type 'int [3]'"} | {"equals": "DENIED"} |
| trailing text | robustness | {"equals": "20"} | {"equals": "DENIED"} |
| fractional index | robustness | {"equals": "20"} | {"equals": "DENIED"} |
| exponent notation | robustness | {"equals": "20"} | {"equals": "DENIED"} |
| leading whitespace | robustness | {"equals": "20"} | {"equals": "DENIED"} |
| leading plus | robustness | {"equals": "20"} | {"equals": "DENIED"} |
| empty index | robustness | {"equals": "10"} | {"equals": "DENIED"} |
| nonnumeric index | robustness | {"equals": "10"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
