# Path traversal

A client filename escapes the public directory.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-22 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use a server-side allowlist of filenames in a trusted directory.

## Regression

```sh
python3 tools/lab.py test --case cgi/path-traversal --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| allowed file | benign | {"equals": "Content-Type: application/json\r\n\r\n\"WELCOME\""} | {"equals": "Content-Type: application/json\r\n\r\n\"WELCOME\""} |
| parent directory | attack | {"equals": "Content-Type: application/json\r\n\r\n\"LAB_SECRET\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
