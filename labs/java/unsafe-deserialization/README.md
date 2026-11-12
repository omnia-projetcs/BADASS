# Unsafe deserialization

A Java payload loader accepts serialized class descriptors (CLASS:ExecGadget) and triggers gadget side effects.

| Attribute | Value |
|---|---|
| Technology | Java |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/Main.java) · [Corrected source](fixed/Main.java)

## Correction

Reject polymorphic class descriptors and accept only bounded JSON values matching an explicit allowlist.

## Regression

```sh
python3 tools/lab.py test --case java/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| safe JSON string | benign | {"equals": "hello"} | {"equals": "hello"} |
| serialized gadget descriptor | attack | {"equals": "LAB_GADGET_EXECUTED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
