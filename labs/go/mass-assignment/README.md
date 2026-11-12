# Mass assignment

Unmarshaling client JSON directly into the internal Account struct allows overwriting the exported Role field.

| Attribute | Value |
|---|---|
| Technology | Go |
| CWE | CWE-915 |
| OWASP | A01:2025, API3:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.go) · [Corrected source](fixed/main.go)

## Correction

Unmarshal client input into a dedicated DTO struct containing only user-editable fields.

## Regression

```sh
python3 tools/lab.py test --case go/mass-assignment --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| update display name | benign | {"equals": "Bob:user"} | {"equals": "Bob:user"} |
| privilege escalation via role field | attack | {"equals": "Bob:admin"} | {"equals": "Bob:user"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
