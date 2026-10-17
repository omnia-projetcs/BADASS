# Stack buffer overflow

Unbounded copying overwrites a stack buffer.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-121 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Check the length before copying and preserve room for the terminator.

## Regression

```sh
python3 tools/lab.py test --case c/stack-buffer-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| short input | benign | {"equals": "hello"} | {"equals": "hello"} |
| oversized input | attack | {"stderr_contains": "stack-buffer-overflow"} | {"equals": "DENIED"} |
| empty input | benign | {"equals": ""} | {"equals": ""} |
| last fitting byte | benign | {"equals": "ABCDEFG"} | {"equals": "ABCDEFG"} |
| terminator boundary | attack | {"stderr_contains": "stack-buffer-overflow"} | {"equals": "DENIED"} |
| one byte beyond capacity | attack | {"stderr_contains": "stack-buffer-overflow"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
