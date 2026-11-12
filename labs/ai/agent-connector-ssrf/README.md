# Agent connector SSRF

An AI agent URL-fetch tool permits model-supplied requests to cloud metadata (169.254.169.254) and loopback management endpoints.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-918 |
| OWASP | LLM06:2025, API7:2023 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require HTTPS and validate the parsed hostname, port, and path against an explicit server-side allowlist before dispatching agent connector requests.

## Regression

```sh
python3 tools/lab.py test --case ai/agent-connector-ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| approved documentation URL | benign | {"equals": "PUBLIC_GUIDE"} | {"equals": "PUBLIC_GUIDE"} |
| cloud metadata SSRF | attack | {"equals": "LAB_METADATA_CREDENTIALS"} | {"equals": "DENIED"} |
| loopback admin SSRF | attack | {"equals": "LAB_LOOPBACK_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
