# Fail open

An authorization backend failure is treated as permission.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-636 |
| OWASP | A10:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Deny access when authorization cannot be established.

## Regression

```sh
python3 tools/lab.py test --case python/fail-open --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| authorized | benign | {"equals": true} | {"equals": true} |
| backend failure | attack | {"equals": true} | {"equals": false} |
| unauthorized | benign | {"equals": false} | {"equals": false} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
