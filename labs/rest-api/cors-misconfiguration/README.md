# Credentialed CORS misconfiguration

Credentialed CORS responses reflect any Origin.

**Technology:** REST API (Python handlers)  
**CWE:** CWE-942  
**OWASP:** API8:2023  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allow only known application origins.

## Regression

```sh
python3 tools/lab.py test --case rest-api/cors-misconfiguration --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| approved origin | benign | {"equals": {"Access-Control-Allow-Origin": "https://app.example.test", "Access-Control-Allow-Credentials": "true"}} | {"equals": {"Access-Control-Allow-Origin": "https://app.example.test", "Access-Control-Allow-Credentials": "true"}} |
| foreign origin | attack | {"equals": {"Access-Control-Allow-Origin": "https://attacker.invalid", "Access-Control-Allow-Credentials": "true"}} | {"equals": {}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
