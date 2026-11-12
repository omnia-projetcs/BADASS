# Unsafe deserialization

A Ruby deserialization boundary accepts !ruby/object YAML tags to instantiate arbitrary classes.

| Attribute | Value |
|---|---|
| Technology | Ruby |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.rb) · [Corrected source](fixed/main.rb)

## Correction

Reject YAML object tags and parse untrusted payloads exclusively with JSON.parse and strict key validation.

## Regression

```sh
python3 tools/lab.py test --case ruby/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| JSON user payload | benign | {"equals": "USER:alice"} | {"equals": "USER:alice"} |
| YAML ruby/object gadget | attack | {"equals": "LAB_RUBY_GADGET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
