# Path traversal

A client filename escapes the public directory and reads a synthetic secret.

**Technology:** .NET / C#  
**CWE:** CWE-22  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/Program.cs) · [Corrected source](fixed/Program.cs)

## Correction

Use a server-side filename allowlist. The public directory is trusted and not attacker-writable.

## Regression

```sh
python3 tools/lab.py test --case dotnet/path-traversal --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| allowed file | benign | {"equals": "WELCOME"} | {"equals": "WELCOME"} |
| parent traversal | attack | {"equals": "LAB_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
