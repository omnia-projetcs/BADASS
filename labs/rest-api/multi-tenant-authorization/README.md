# Multi tenant authorization

Two server-owned synthetic sessions authenticate different tenants, but an invoice lookup omits tenant authorization.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-863 |
| OWASP | A01:2025, API1:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Resolve the principal through the trusted session table and authorize the resource tenant; ignore request-supplied identity and role hints.

## Regression

```sh
python3 tools/lab.py test --case rest-api/multi-tenant-authorization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| Alice reads the north invoice | benign | {"equals": {"status": 200, "body": {"id": "invoice-north", "tenant_id": "north", "total": 10, "memo": "LAB_NORTH_INVOICE"}}} | {"equals": {"status": 200, "body": {"id": "invoice-north", "tenant_id": "north", "total": 10, "memo": "LAB_NORTH_INVOICE"}}} |
| Bob reads the south invoice | benign | {"equals": {"status": 200, "body": {"id": "invoice-south", "tenant_id": "south", "total": 900, "memo": "LAB_SOUTH_INVOICE"}}} | {"equals": {"status": 200, "body": {"id": "invoice-south", "tenant_id": "south", "total": 900, "memo": "LAB_SOUTH_INVOICE"}}} |
| unknown invoice | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| Alice crosses into the south tenant | attack | {"equals": {"status": 200, "body": {"id": "invoice-south", "tenant_id": "south", "total": 900, "memo": "LAB_SOUTH_INVOICE"}}} | {"equals": {"status": 404}} |
| Bob crosses into the north tenant | attack | {"equals": {"status": 200, "body": {"id": "invoice-north", "tenant_id": "north", "total": 10, "memo": "LAB_NORTH_INVOICE"}}} | {"equals": {"status": 404}} |
| body identity hints cannot expand the session | attack | {"equals": {"status": 200, "body": {"id": "invoice-south", "tenant_id": "south", "total": 900, "memo": "LAB_SOUTH_INVOICE"}}} | {"equals": {"status": 404}} |
| unrecognized session is unauthenticated | robustness | {"equals": {"status": 401}} | {"equals": {"status": 401}} |
| invoice id must be a string | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
