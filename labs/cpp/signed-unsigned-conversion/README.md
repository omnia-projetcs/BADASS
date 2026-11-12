# Signed unsigned conversion

Converting a negative signed integer to unsigned int after an upper-bound check produces a massive unsigned size.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-195, CWE-681 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Enforce strict positive integer parsing and verify 1 <= requested <= 64 prior to static_cast<unsigned int>.

## Regression

```sh
python3 tools/lab.py test --case cpp/signed-unsigned-conversion --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid chunk size | benign | {"equals": "COPIED:16"} | {"equals": "COPIED:16"} |
| negative length wraparound | attack | {"equals": "OVERFLOW_LEN:4294967295"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
