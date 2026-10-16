# Disabled TLS verification

The client TLS context disables certificate verification.

**Technology:** Python  
**CWE:** CWE-295  
**OWASP:** A04:2025  
**Test scope:** `configuration-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use the system trust store with certificate and hostname verification enabled.

## Regression

```sh
python3 tools/lab.py test --case python/tls-verification --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| no connection | benign | {"equals": "OK"} | {"equals": "OK"} |
| TLS configuration | attack | {"equals": false} | {"equals": true} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
