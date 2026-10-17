# Command injection

A client value is concatenated into a shell command.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-78 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Pass the value as one argument to a fixed executable without a shell.

## Regression

```sh
python3 tools/lab.py test --case rest-api/command-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary argument | benign | {"equals": "hello"} | {"equals": "hello"} |
| shell command | attack | {"equals": "helloBADASS_INJECTED"} | {"equals": "hello; printf BADASS_INJECTED"} |
| spaces in an argument | functional | {"equals": "helloworld"} | {"equals": "hello world"} |
| leading and trailing whitespace | functional | {"equals": "helloworld"} | {"equals": "  hello\tworld  "} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
