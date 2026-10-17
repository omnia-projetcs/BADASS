# Path traversal

A client filename escapes the public directory and reads a synthetic secret.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-22 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Use a server-side filename allowlist. The public directory is trusted and not attacker-writable.

## Regression

```sh
python3 tools/lab.py test --case node/path-traversal --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| allowed file | benign | {"equals": "WELCOME"} | {"equals": "WELCOME"} |
| parent traversal | attack | {"equals": "LAB_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
