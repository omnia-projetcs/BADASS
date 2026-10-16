# Server-side request forgery (SSRF)

A server-side fetch reaches a private endpoint controlled by client input.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-918  
**OWASP:** API7:2023  
**Test scope:** `loopback-integration`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allowlist a fixed upstream endpoint; production also needs DNS, redirect and egress controls.

## Regression

```sh
python3 tools/lab.py test --case rest-api/ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public endpoint | benign | {"equals": "PUBLIC"} | {"equals": "PUBLIC"} |
| internal endpoint | attack | {"equals": "LAB_INTERNAL_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
