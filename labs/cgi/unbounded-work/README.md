# Unbounded work

A client controls memory allocation without an application budget.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-400 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the requested size and enforce a limit before allocating.

## Regression

```sh
python3 tools/lab.py test --case cgi/unbounded-work --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| small allocation | benign | {"equals": "Content-Type: application/json\r\n\r\n\"10\""} | {"equals": "Content-Type: application/json\r\n\r\n\"10\""} |
| limit boundary | benign | {"equals": "Content-Type: application/json\r\n\r\n\"100\""} | {"equals": "Content-Type: application/json\r\n\r\n\"100\""} |
| over budget | attack | {"equals": "Content-Type: application/json\r\n\r\n\"101\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| large request | attack | {"equals": "Content-Type: application/json\r\n\r\n\"1000\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
