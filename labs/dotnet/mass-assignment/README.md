# Mass assignment

Binding untrusted JSON directly to a .NET account entity allows the caller to set the privileged role property.

| Attribute | Value |
|---|---|
| Technology | .NET / C# |
| CWE | CWE-915 |
| OWASP | A01:2025, API3:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/Program.cs) · [Corrected source](fixed/Program.cs)

## Correction

Bind incoming JSON to a dedicated update DTO exposing only the editable name property.

## Regression

```sh
python3 tools/lab.py test --case dotnet/mass-assignment --strict
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
