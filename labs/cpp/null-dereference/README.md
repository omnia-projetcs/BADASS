# Null dereference

An absent object is dereferenced without checking its pointer.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-476 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Validate the pointer before reading the object.

## Regression

```sh
python3 tools/lab.py test --case cpp/null-dereference --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid lifetime or length | benign | {"equals": "42"} | {"equals": "42"} |
| invalid lifetime or length | attack | {"stderr_contains": "load of null pointer"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
