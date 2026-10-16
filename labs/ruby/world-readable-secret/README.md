# World readable secret

A secret file receives permissions allowing other users to read it.

**Technology:** Ruby  
**CWE:** CWE-732  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.rb) · [Corrected source](fixed/main.rb)

## Correction

Create sensitive files with owner-only permissions and retain those permissions.

## Regression

```sh
python3 tools/lab.py test --case ruby/world-readable-secret --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public file | benign | {"equals": "0644"} | {"equals": "0644"} |
| private file | attack | {"equals": "0644"} | {"equals": "0600"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
