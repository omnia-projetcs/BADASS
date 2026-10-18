# Tenant signed download

A bearer download grant authenticates a local document ID and expiry but omits its tenant. An authorized requester changes only the tenant during redemption and reads a different organization's document with the same ID. The fixture computes a real HMAC with a fresh server-owned key.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-863 |
| OWASP | A01:2025, API1:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Sign and verify the action, tenant, document identifier and expiration as one unambiguously serialized tuple. Authenticated issuance is scoped to the server session; redemption is an intentionally shareable bearer capability. One invocation models issuance followed by redemption using a pinned clock. Key distribution, revocation and HTTP delivery are outside this local flow.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-signed-download --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| north intended document | benign | {"equals": {"status": 200, "content": "LAB_NORTH_SHARED_REPORT"}} | {"equals": {"status": 200, "content": "LAB_NORTH_SHARED_REPORT"}} |
| south intended document | benign | {"equals": {"status": 200, "content": "LAB_SOUTH_SHARED_REPORT"}} | {"equals": {"status": 200, "content": "LAB_SOUTH_SHARED_REPORT"}} |
| different authorized document | benign | {"equals": {"status": 200, "content": "LAB_NORTH_SHARED_NOTES"}} | {"equals": {"status": 200, "content": "LAB_NORTH_SHARED_NOTES"}} |
| replace north with south | attack | {"equals": {"status": 200, "content": "LAB_SOUTH_SHARED_REPORT"}} | {"equals": {"status": 403}} |
| replace south with north | attack | {"equals": {"status": 200, "content": "LAB_NORTH_SHARED_REPORT"}} | {"equals": {"status": 403}} |
| forged issuer tenant field | attack | {"equals": {"status": 200, "content": "LAB_SOUTH_SHARED_REPORT"}} | {"equals": {"status": 403}} |
| alter document invalidates signature | benign | {"equals": {"status": 403}} | {"equals": {"status": 403}} |
| cannot issue foreign-only document | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| invalid session | benign | {"equals": {"status": 401}} | {"equals": {"status": 401}} |
| missing fields | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| non-object input | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| non-string tenant | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| oversized document | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [OWASP — Multi-Tenant Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
