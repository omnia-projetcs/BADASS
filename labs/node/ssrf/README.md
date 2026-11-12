# Server-side request forgery (SSRF)

A Node.js URL fetch handler permits requests to 169.254.169.254 and loopback targets supplied by the caller.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-918 |
| OWASP | A01:2025, API7:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Validate the parsed URL protocol, hostname, port, and pathname against an explicit server-side allowlist.

## Regression

```sh
python3 tools/lab.py test --case node/ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| approved status URL | benign | {"equals": "PUBLIC_OK"} | {"equals": "PUBLIC_OK"} |
| metadata endpoint SSRF | attack | {"equals": "LAB_INTERNAL_METADATA"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
