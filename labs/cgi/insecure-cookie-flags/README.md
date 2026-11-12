# Insecure cookie flags

The CGI response sets a sensitive session cookie without the Secure, HttpOnly, and SameSite=Strict attributes.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-614, CWE-1004, CWE-1275 |
| OWASP | A02:2025, A07:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the session identifier format and append Secure, HttpOnly, and SameSite=Strict to every session Set-Cookie header.

## Regression

```sh
python3 tools/lab.py test --case cgi/insecure-cookie-flags --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| health ping | benign | {"equals": "Status: 200 OK\r\nContent-Type: text/plain\r\n\r\nPONG"} | {"equals": "Status: 200 OK\r\nContent-Type: text/plain\r\n\r\nPONG"} |
| session cookie attributes | attack | {"equals": "Set-Cookie: session=LABSESSION1234; Path=/\r\nContent-Type: text/plain\r\n\r\nOK"} | {"equals": "Set-Cookie: session=LABSESSION1234; Path=/; Secure; HttpOnly; SameSite=Strict\r\nContent-Type: text/plain\r\n\r\nOK"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
