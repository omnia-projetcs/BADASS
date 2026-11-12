# Type confusion

Accessing an inactive C++ union member without checking the record discriminant confuses a user number with a service privilege flag.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-843 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Enforce discriminant checks before accessing union fields and validate numeric ranges prior to assignment.

## Regression

```sh
python3 tools/lab.py test --case cpp/type-confusion --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| guest principal | benign | {"equals": "GUEST:42"} | {"equals": "GUEST:42"} |
| union tag confusion | attack | {"equals": "ADMIN"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
