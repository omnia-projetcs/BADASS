# Double free

Two cleanup paths release the same allocation.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-415 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Release the object once and clear the pointer before another cleanup path.

## Regression

```sh
python3 tools/lab.py test --case c/double-free --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid lifetime or length | benign | {"equals": "OK"} | {"equals": "OK"} |
| invalid lifetime or length | attack | {"stderr_contains": "attempting double-free"} | {"equals": "OK"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
