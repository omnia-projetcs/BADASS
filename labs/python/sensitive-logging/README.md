# Sensitive logging

Authentication logs retain a supplied password.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-532 |
| OWASP | A09:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Log an allowlisted event schema that omits credentials.

## Regression

```sh
python3 tools/lab.py test --case python/sensitive-logging --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| safe event | benign | {"equals": {"event": "login", "user": "alice"}} | {"equals": {"event": "login", "user": "alice"}} |
| credential in log | attack | {"equals": {"event": "login", "password": "LAB_SECRET"}} | {"equals": {"event": "login"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
