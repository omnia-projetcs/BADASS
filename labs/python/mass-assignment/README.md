# Mass assignment

Unrestricted profile updates overwrite a privileged role.

**Technology:** Python  
**CWE:** CWE-915  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allowlist user-editable profile properties.

## Regression

```sh
python3 tools/lab.py test --case python/mass-assignment --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| display name | benign | {"equals": {"name": "Bob", "role": "user"}} | {"equals": {"name": "Bob", "role": "user"}} |
| role change | attack | {"equals": {"name": "Alice", "role": "admin"}} | {"equals": {"name": "Alice", "role": "user"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
