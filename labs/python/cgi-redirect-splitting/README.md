# CGI redirect response splitting

A CGI query parameter is URL-decoded and inserted into a serialized HTTP Location header. CRLF sequences create extra headers or terminate the header block. Inspired by EDB-49923; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-113 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject every control character after query decoding and before response serialization. This is a response-serialization fixture with no live HTTP server or browser; it demonstrates header/body boundaries, not script execution.

## Regression

```sh
python3 tools/lab.py test --case python/cgi-redirect-splitting --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal redirect | benign | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\nContent-Length: 0\r\n\r\n"} | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\nContent-Length: 0\r\n\r\n"} |
| encoded slash | benign | {"equals": "HTTP/1.1 302 Found\r\nLocation: /settings\r\nContent-Length: 0\r\n\r\n"} | {"equals": "HTTP/1.1 302 Found\r\nLocation: /settings\r\nContent-Length: 0\r\n\r\n"} |
| extra query parameter | benign | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\nContent-Length: 0\r\n\r\n"} | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\nContent-Length: 0\r\n\r\n"} |
| injected response header | attack | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\nX-Lab: injected\r\nContent-Length: 0\r\n\r\n"} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| response body injection | attack | {"equals": "HTTP/1.1 302 Found\r\nLocation: settings.htm\r\n\r\nLAB_BODY\r\nContent-Length: 0\r\n\r\n"} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| LF header injection | attack | {"equals": "HTTP/1.1 302 Found\r\nLocation: x\nX-Lab: y\r\nContent-Length: 0\r\n\r\n"} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| duplicate redirect | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| missing redirect | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| bad UTF8 | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| wrong type | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-49923 — CHIYU TCP/IP Converter devices — CRLF injection (sirpedrotavares)](https://www.exploit-db.com/exploits/49923)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
