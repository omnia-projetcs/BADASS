# Broken authentication

Any nonempty bearer value is accepted as authentication.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-287  
**OWASP:** API2:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the full credential against a server-side credential store.

## Regression

```sh
python3 tools/lab.py test --case rest-api/broken-authentication --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid token | benign | {"equals": {"status": 200}} | {"equals": {"status": 200}} |
| forged token | attack | {"equals": {"status": 200}} | {"equals": {"status": 401}} |
| missing token | benign | {"equals": {"status": 401}} | {"equals": {"status": 401}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
