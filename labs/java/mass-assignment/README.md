# Mass assignment

Automatic property binding on a Java account model binds the privileged role parameter from client input.

| Attribute | Value |
|---|---|
| Technology | Java |
| CWE | CWE-915 |
| OWASP | A01:2025, API3:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/Main.java) · [Corrected source](fixed/Main.java)

## Correction

Restrict data binding to an explicit allowlist of editable fields (name) and ignore or reject role parameters.

## Regression

```sh
python3 tools/lab.py test --case java/mass-assignment --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| update display name | benign | {"equals": "Bob:user"} | {"equals": "Bob:user"} |
| privilege escalation via role parameter | attack | {"equals": "Bob:admin"} | {"equals": "Bob:user"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
