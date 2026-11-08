# Backslash open redirect

A local-path redirect check allows a slash followed by a backslash. Browsers interpreting backslashes as separators can treat the resulting Location as a network-path reference to an external host. Inspired by EDB-43592; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-601 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

After one strict percent-decoding pass, reject backslashes, control characters, residual percent encodings and any URL authority or scheme; allow only absolute local paths beginning with a single slash. Output is a Location model with no live browser. Tests normalize the browser separator behavior explicitly; this is not a complete WHATWG URL parser.

## Regression

```sh
python3 tools/lab.py test --case python/backslash-open-redirect --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| local dashboard | benign | {"equals": {"status": 302, "location": "/dashboard"}} | {"equals": {"status": 302, "location": "/dashboard"}} |
| encoded local path | benign | {"equals": {"status": 302, "location": "/docs/help"}} | {"equals": {"status": 302, "location": "/docs/help"}} |
| local query | benign | {"equals": {"status": 302, "location": "/search?q=test"}} | {"equals": {"status": 302, "location": "/search?q=test"}} |
| external URL denied | benign | {"equals": {"status": 403, "error": "external redirect"}} | {"equals": {"status": 403, "error": "external redirect"}} |
| network path denied | benign | {"equals": {"status": 403, "error": "external redirect"}} | {"equals": {"status": 403, "error": "external redirect"}} |
| backslash authority | attack | {"equals": {"status": 302, "location": "/\\evil.test/path"}} | {"equals": {"status": 403, "error": "external redirect"}} |
| encoded backslash authority | attack | {"equals": {"status": 302, "location": "/\\evil.test/path"}} | {"equals": {"status": 403, "error": "external redirect"}} |
| double encoded separator rejected | functional | {"equals": {"status": 302, "location": "/%5Cevil.test/path"}} | {"equals": {"status": 403, "error": "external redirect"}} |
| CRLF rejected | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| wrong input type | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |
| bad UTF8 | robustness | {"equals": {"status": 400, "error": "invalid redirect"}} | {"equals": {"status": 400, "error": "invalid redirect"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-43592 — Oracle E-Business Suite — backslash open redirect / CVE-2017-3528 (Andrew Gill)](https://www.exploit-db.com/exploits/43592)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
