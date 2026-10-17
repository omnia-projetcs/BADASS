# Symlink following

An export follows a preplaced symbolic link and overwrites a private file.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-59 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Use atomic exclusive creation; reject an existing final path instead of following it. The parent directory is trusted.

## Regression

```sh
python3 tools/lab.py test --case node/symlink-following --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary export | benign | {"equals": "LAB_SECRET", "files": [{"path": "secret.txt", "type": "file", "content": "LAB_SECRET"}, {"path": "export.tmp", "type": "file", "content": "LAB_OVERWRITTEN"}]} | {"equals": "LAB_SECRET", "files": [{"path": "secret.txt", "type": "file", "content": "LAB_SECRET"}, {"path": "export.tmp", "type": "file", "content": "LAB_OVERWRITTEN"}]} |
| preplaced link | attack | {"equals": "LAB_OVERWRITTEN", "files": [{"path": "secret.txt", "type": "file", "content": "LAB_OVERWRITTEN"}, {"path": "export.tmp", "type": "symlink", "target": "secret.txt"}]} | {"equals": "LAB_SECRET", "files": [{"path": "secret.txt", "type": "file", "content": "LAB_SECRET"}, {"path": "export.tmp", "type": "symlink", "target": "secret.txt"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
