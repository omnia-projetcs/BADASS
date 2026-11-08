# Open redirect

A client-selected destination produces an external redirect.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-601 |
| OWASP | A01:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allowlist complete application-local destinations, including rejection of scheme-relative URLs.

## Regression

```sh
python3 tools/lab.py test --case cgi/open-redirect --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| local home | benign | {"equals": "Location: /home\r\n\r\n"} | {"equals": "Location: /home\r\n\r\n"} |
| local profile | benign | {"equals": "Location: /profile\r\n\r\n"} | {"equals": "Location: /profile\r\n\r\n"} |
| external destination | attack | {"equals": "Location: https://attacker.invalid\r\n\r\n"} | {"equals": "Status: 400 Bad Request\r\n\r\n"} |
| scheme-relative destination | attack | {"equals": "Location: //attacker.invalid\r\n\r\n"} | {"equals": "Status: 400 Bad Request\r\n\r\n"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
