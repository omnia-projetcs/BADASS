# HTTP response header injection

An untrusted display name injects another HTTP response header.

| Attribute | Value |
|---|---|
| Technology | PHP |
| CWE | CWE-113 |
| OWASP | A05:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.php) · [Corrected source](fixed/main.php)

## Correction

Reject carriage returns and line feeds before constructing header fields.

## Regression

```sh
python3 tools/lab.py test --case php/header-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary header | benign | {"equals": "X-User: alice\n\nBODY"} | {"equals": "X-User: alice\n\nBODY"} |
| CRLF header | attack | {"equals": "X-User: alice\nX-Admin: true\n\nBODY"} | {"equals": "DENIED"} |
| LF header | attack | {"equals": "X-User: alice\nX-Admin: true\n\nBODY"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
