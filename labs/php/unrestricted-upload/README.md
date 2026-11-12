# Unrestricted upload

A PHP upload handler stores files with executable .php and double extensions (.php.phtml) in the upload directory.

| Attribute | Value |
|---|---|
| Technology | PHP |
| CWE | CWE-434 |
| OWASP | A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.php) · [Corrected source](fixed/main.php)

## Correction

Validate the entire filename against a strict single-extension allowlist (.txt, .png) before storing.

## Regression

```sh
python3 tools/lab.py test --case php/unrestricted-upload --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| safe text upload | benign | {"equals": "SAVED:report.txt"} | {"equals": "SAVED:report.txt"} |
| executable PHP script upload | attack | {"equals": "SAVED:shell.php"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
