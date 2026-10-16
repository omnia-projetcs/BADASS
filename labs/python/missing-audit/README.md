# Missing security audit events

Denied administrative actions produce no security audit event.

**Technology:** Python  
**CWE:** CWE-778  
**OWASP:** A09:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Emit structured denied-action events without sensitive input.

## Regression

```sh
python3 tools/lab.py test --case python/missing-audit --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| health | benign | {"equals": {"status": 200, "audit": []}} | {"equals": {"status": 200, "audit": []}} |
| denied admin | attack | {"equals": {"status": 403, "audit": []}} | {"equals": {"status": 403, "audit": [{"event": "admin_access_denied", "actor": "alice"}]}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
