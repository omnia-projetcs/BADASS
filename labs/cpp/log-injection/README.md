# Log injection

A username containing line breaks forges another audit record.

| Attribute | Value |
|---|---|
| Technology | C++ |
| CWE | CWE-117 |
| OWASP | A09:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Escape backslashes and line-break characters before writing line-oriented audit records.

## Regression

```sh
python3 tools/lab.py test --case cpp/log-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal username | benign | {"equals": "user=alice"} | {"equals": "user=alice"} |
| forged audit event | attack | {"equals": "user=alice\nADMIN_LOGIN"} | {"equals": "user=alice\\nADMIN_LOGIN"} |
| CRLF audit event | attack | {"equals": "user=alice\nADMIN_LOGIN"} | {"equals": "user=alice\\r\\nADMIN_LOGIN"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
