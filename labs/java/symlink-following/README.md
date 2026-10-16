# Symlink following

An export follows a preplaced symbolic link and overwrites a private file.

**Technology:** Java  
**CWE:** CWE-59  
**OWASP:** A01:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/Main.java) · [Corrected source](fixed/Main.java)

## Correction

Use atomic exclusive creation; reject an existing final path instead of following it. The parent directory is trusted.

## Regression

```sh
python3 tools/lab.py test --case java/symlink-following --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary export | benign | {"equals": "LAB_SECRET"} | {"equals": "LAB_SECRET"} |
| preplaced link | attack | {"equals": "LAB_OVERWRITTEN"} | {"equals": "LAB_SECRET"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
