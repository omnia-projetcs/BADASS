# World readable secret

A secret file receives permissions allowing other users to read it.

| Attribute | Value |
|---|---|
| Technology | Java |
| CWE | CWE-732 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/Main.java) · [Corrected source](fixed/Main.java)

## Correction

Create sensitive files with owner-only permissions and retain those permissions.

## Regression

```sh
python3 tools/lab.py test --case java/world-readable-secret --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public file | benign | {"equals": "0644", "files": [{"path": "stored-secret", "type": "file", "content": "PUBLIC", "mode": "0644"}]} | {"equals": "0644", "files": [{"path": "stored-secret", "type": "file", "content": "PUBLIC", "mode": "0644"}]} |
| private file | attack | {"equals": "0644", "files": [{"path": "stored-secret", "type": "file", "content": "LAB_SECRET", "mode": "0644"}]} | {"equals": "0600", "files": [{"path": "stored-secret", "type": "file", "content": "LAB_SECRET", "mode": "0600"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
