# Business logic

A negative purchase quantity increases the account balance.

**Technology:** CGI (Python)  
**CWE:** CWE-841  
**OWASP:** A06:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce positive bounded purchase quantities before changing the balance.

## Regression

```sh
python3 tools/lab.py test --case cgi/business-logic --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary order | benign | {"equals": "Content-Type: application/json\r\n\r\n\"980\""} | {"equals": "Content-Type: application/json\r\n\r\n\"980\""} |
| boundary order | benign | {"equals": "Content-Type: application/json\r\n\r\n\"0\""} | {"equals": "Content-Type: application/json\r\n\r\n\"0\""} |
| negative order | attack | {"equals": "Content-Type: application/json\r\n\r\n\"1050\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| zero order | attack | {"equals": "Content-Type: application/json\r\n\r\n\"1000\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
