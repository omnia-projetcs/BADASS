# HTTP response header injection

A decoded CGI parameter injects response headers.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-113 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject carriage returns and line feeds in header values.

## Regression

```sh
python3 tools/lab.py test --case cgi/header-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary location | benign | {"equals": "Location: /home\r\n\r\n"} | {"equals": "Location: /home\r\n\r\n"} |
| injected header | attack | {"equals": "Location: /home\r\nX-Lab: injected\r\n\r\n"} | {"equals": "Status: 400 Bad Request\r\n\r\n"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
