# SSRF through an HTTP redirect

An approved local endpoint redirects a server-side fetch to a private resource.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-918 |
| OWASP | API7:2023 |
| Test scope | `loopback-integration` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Disable automatic redirects and validate every resolved destination before requesting it. Bound redirect count and request duration. This fixture uses a fixed loopback address and port; production DNS resolution, address ranges and egress policy need separate controls.

## Regression

```sh
python3 tools/lab.py test --case rest-api/ssrf-redirect --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public endpoint | benign | {"equals": "PUBLIC", "files": [{"path": "http-access.log", "content": "/public\n"}]} | {"equals": "PUBLIC", "files": [{"path": "http-access.log", "content": "/public\n"}]} |
| approved redirect | benign | {"equals": "PUBLIC", "files": [{"path": "http-access.log", "content": "/redirect-public\n/public\n"}]} | {"equals": "PUBLIC", "files": [{"path": "http-access.log", "content": "/redirect-public\n/public\n"}]} |
| redirect to private resource | attack | {"equals": "LAB_INTERNAL_SECRET", "files": [{"path": "http-access.log", "content": "/redirect-private\n/internal\n"}]} | {"equals": "DENIED", "files": [{"path": "http-access.log", "content": "/redirect-private\n"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
