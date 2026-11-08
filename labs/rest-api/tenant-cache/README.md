# Tenant cache

A shared response cache uses a tenant-local document identifier as its entire key. Origin lookups are scoped correctly, but a cache hit can expose the previous tenant's document. A bounded sequence models authenticated requests sharing one live cache.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-488 |
| OWASP | A01:2025, API1:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Authenticate before cache access and include the server-owned tenant in the cache key. All users in one tenant share the same document policy in this fixture. A production cache must also represent any user, role, authorization version or representation dimension that changes visibility; TTL, revocation and distributed caching are not modeled.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-cache --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| north miss | benign | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} |
| south miss | benign | {"equals": {"responses": [{"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}]}} |
| same tenant cache hit | benign | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} |
| distinct documents | benign | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_INVOICE"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_INVOICE"}]}} |
| authentication before hit | benign | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 401}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 401}]}} |
| unknown document | benign | {"equals": {"responses": [{"status": 404}]}} | {"equals": {"responses": [{"status": 404}]}} |
| north then south | attack | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}]}} |
| south then north | attack | {"equals": {"responses": [{"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} |
| body cannot select authenticated tenant | attack | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}]}} | {"equals": {"responses": [{"status": 200, "content": "LAB_NORTH_PRIVATE_SUMMARY"}, {"status": 200, "content": "LAB_SOUTH_PRIVATE_SUMMARY"}]}} |
| missing sequence | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| empty sequence | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| too many requests | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| bad document type | robustness | {"equals": {"responses": [{"status": 400}]}} | {"equals": {"responses": [{"status": 400}]}} |
| non-object item | robustness | {"equals": {"responses": [{"status": 400}]}} | {"equals": {"responses": [{"status": 400}]}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-488 — Exposure of Data Element to Wrong Session](https://cwe.mitre.org/data/definitions/488.html)
- [OWASP API1:2023 — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
