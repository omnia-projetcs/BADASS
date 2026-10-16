# Weak password hash

Passwords are stored with unsalted fast MD5.

**Technology:** Python  
**CWE:** CWE-916  
**OWASP:** A04:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use a salted, costed password KDF; this example uses scrypt.

## Regression

```sh
python3 tools/lab.py test --case python/weak-password-hash --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty password | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| password storage | attack | {"equals": {"password_matches": true, "legacy_md5": true}} | {"equals": {"password_matches": true, "legacy_md5": false}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
