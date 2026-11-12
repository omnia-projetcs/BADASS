# Unsafe slice bounds

An unsafe get_unchecked() call bypasses Rust's slice length check and reads an adjacent out-of-slice element.

| Attribute | Value |
|---|---|
| Technology | Rust |
| CWE | CWE-119, CWE-125 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.rs) · [Corrected source](fixed/main.rs)

## Correction

Eliminate the unsafe block and use safe slice.get(idx) bounds checking.

## Regression

```sh
python3 tools/lab.py test --case rust/unsafe-slice-bounds --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| in-bounds slice index | benign | {"equals": "20"} | {"equals": "20"} |
| out-of-slice unchecked read | attack | {"equals": "9999"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
