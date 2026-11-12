# Unsafe deserialization

Passing untrusted input to PHP unserialize() instantiates an attacker-supplied object with privileged properties.

| Attribute | Value |
|---|---|
| Technology | PHP |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.php) · [Corrected source](fixed/main.php)

## Correction

Replace unserialize() with json_decode() and validate the decoded associative array against a strict schema.

## Regression

```sh
python3 tools/lab.py test --case php/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| JSON user record | benign | {"equals": "USER:alice"} | {"equals": "USER:alice"} |
| serialized PHP object payload | attack | {"equals": "ADMIN_GADGET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
