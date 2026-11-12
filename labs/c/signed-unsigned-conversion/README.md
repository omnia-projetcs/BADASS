# Signed unsigned conversion

A signed upper-bound check passes a negative integer that wraps into a large unsigned length upon conversion.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-195, CWE-681 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Validate both lower (>= 1) and upper (<= 64) bounds on the parsed signed integer before casting to an unsigned type.

## Regression

```sh
python3 tools/lab.py test --case c/signed-unsigned-conversion --strict
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
