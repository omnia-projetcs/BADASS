# Broken object-level authorization (BOLA)

An authenticated API caller reads an invoice owned by another user.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-639  
**OWASP:** API1:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Scope object lookup to the authenticated principal.

## Regression

```sh
python3 tools/lab.py test --case rest-api/bola --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| own invoice | benign | {"equals": {"status": 200, "body": {"owner": "alice", "total": 10}}} | {"equals": {"status": 200, "body": {"owner": "alice", "total": 10}}} |
| other invoice | attack | {"equals": {"status": 200, "body": {"owner": "bob", "total": 900}}} | {"equals": {"status": 404}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
