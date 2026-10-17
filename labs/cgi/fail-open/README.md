# Fail open

An authorization backend error grants access.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-636 |
| OWASP | A10:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Treat an indeterminate authorization result as denial.

## Regression

```sh
python3 tools/lab.py test --case cgi/fail-open --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| authorized caller | benign | {"equals": "Content-Type: application/json\r\n\r\n\"ALLOWED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"ALLOWED\""} |
| unauthorized caller | benign | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| backend failure | attack | {"equals": "Content-Type: application/json\r\n\r\n\"ALLOWED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
