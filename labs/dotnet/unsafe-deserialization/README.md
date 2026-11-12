# Unsafe deserialization

A .NET serializer honors untrusted $type metadata in JSON input to instantiate arbitrary runtime types.

| Attribute | Value |
|---|---|
| Technology | .NET / C# |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/Program.cs) · [Corrected source](fixed/Program.cs)

## Correction

Forbid $type polymorphic type resolution and parse input with System.Text.Json against a fixed schema.

## Regression

```sh
python3 tools/lab.py test --case dotnet/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| standard DTO payload | benign | {"equals": "alice"} | {"equals": "alice"} |
| polymorphic $type gadget | attack | {"equals": "LAB_GADGET_EXECUTED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
