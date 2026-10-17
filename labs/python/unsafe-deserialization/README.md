# Unsafe deserialization

A pickle payload invokes an attacker-selected callable.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject executable serialization and use a typed JSON contract.

## Regression

```sh
python3 tools/lab.py test --case python/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| JSON string | benign | {"equals": "hello"} | {"equals": "hello"} |
| executable pickle | attack | {"equals": "LAB_EXECUTED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
