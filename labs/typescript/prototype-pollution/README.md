# Prototype pollution

Assigning an untrusted __proto__ property changes an object prototype.

**Technology:** TypeScript  
**CWE:** CWE-1321  
**OWASP:** A08:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.ts) · [Corrected source](fixed/main.ts)

## Correction

Build a prototype-free object and reject prototype-related keys.

## Regression

```sh
python3 tools/lab.py test --case typescript/prototype-pollution --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary property | benign | {"equals": "USER"} | {"equals": "USER"} |
| prototype property | attack | {"equals": "ADMIN"} | {"equals": "USER"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
