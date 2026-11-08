# Apache HTTP Server: proxy request splitting

Original reduced Python model inspired by CVE-2023-25690. A rewrite handler decodes a client target and reinserts it into a serialized backend request. CRLF data turns one frontend input into two requests parsed by a real bounded backend parser. Tests observe serialized bytes on disk. This models request splitting, not Apache configuration, live sockets, chunked bodies or a full proxy deployment.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-444 |
| CVE | CVE-2023-25690 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject controls and spaces after URL decoding and before interpolating the rewritten target. Keep validation and serialization on the same representation. The backend parser is a deliberately small GET/header grammar and does not claim HTTP compliance or coverage of all request-smuggling variants. Actual remediation requires the Apache HTTP Server fix and review of affected rewrite rules.

## Regression

```sh
python3 tools/lab.py test --case python/apache-proxy-request-splitting --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary rewritten target | benign | {"equals": {"status": 200, "requests": ["/backend?q=report"]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=report HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} | {"equals": {"status": 200, "requests": ["/backend?q=report"]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=report HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} |
| encoded ordinary character | benign | {"equals": {"status": 200, "requests": ["/backend?q=report"]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=report HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} | {"equals": {"status": 200, "requests": ["/backend?q=report"]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=report HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} |
| empty target | benign | {"equals": {"status": 200, "requests": ["/backend?q="]}, "files": [{"path": "upstream.http", "content": "GET /backend?q= HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} | {"equals": {"status": 200, "requests": ["/backend?q="]}, "files": [{"path": "upstream.http", "content": "GET /backend?q= HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} |
| second administrative request | attack | {"equals": {"status": 200, "requests": ["/backend?q=public", "/admin?x="]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=public HTTP/1.1\r\nHost: backend.test\r\n\r\nGET /admin?x= HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} | {"equals": {"status": 400, "error": "invalid proxy target"}, "files": [{"path": "upstream.http", "type": "absent"}]} |
| alternate internal endpoint | attack | {"equals": {"status": 200, "requests": ["/backend?q=one", "/private?x="]}, "files": [{"path": "upstream.http", "content": "GET /backend?q=one HTTP/1.1\r\nHost: backend.test\r\n\r\nGET /private?x= HTTP/1.1\r\nHost: backend.test\r\n\r\n"}]} | {"equals": {"status": 400, "error": "invalid proxy target"}} |
| malformed request text | robustness | {"equals": {"status": 400, "error": "invalid proxy target"}} | {"equals": {"status": 400, "error": "invalid proxy target"}} |
| non-ASCII target | robustness | {"equals": {"status": 400, "error": "invalid proxy target"}} | {"equals": {"status": 400, "error": "invalid proxy target"}} |
| wrong request type | robustness | {"equals": {"status": 400, "error": "invalid proxy target"}} | {"equals": {"status": 400, "error": "invalid proxy target"}} |
| oversized target | robustness | {"equals": {"status": 400, "error": "invalid proxy target"}} | {"equals": {"status": 400, "error": "invalid proxy target"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Apache HTTP Server CNA record CVE-2023-25690 — rewrite/proxy request splitting](https://httpd.apache.org/security/json/CVE-2023-25690.json)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
