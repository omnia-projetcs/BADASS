# Uninitialized memory

An uninitialized C++ session state member on an unexpected input branch grants elevated privileges.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-457 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Use default member initialization (false) and reject unrecognized role strings before reading session privileges.

## Regression

```sh
python3 tools/lab.py test --case cpp/uninitialized-memory --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal user role | benign | {"equals": "USER"} | {"equals": "USER"} |
| unhandled role branch | attack | {"equals": "ADMIN"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
