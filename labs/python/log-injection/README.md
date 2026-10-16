# Log injection

An untrusted username forges an extra audit event.

**Technology:** Python  
**CWE:** CWE-117  
**OWASP:** A09:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Encode control characters before writing line-oriented audit records.

## Regression

```sh
python3 tools/lab.py test --case python/log-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary name | benign | {"equals": "user=alice"} | {"equals": "user=alice"} |
| forged event | attack | {"equals": "user=alice\nADMIN_LOGIN"} | {"equals": "user=alice\\nADMIN_LOGIN"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
