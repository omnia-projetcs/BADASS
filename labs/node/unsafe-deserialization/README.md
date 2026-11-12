# Unsafe deserialization

A Node.js deserializer evaluates node-serialize style _$$ND_FUNC$$_ function markers embedded in JSON objects.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-502 |
| OWASP | A08:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Parse input with standard JSON.parse, reject function serialization markers, and validate scalar field formats.

## Regression

```sh
python3 tools/lab.py test --case node/unsafe-deserialization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain string value | benign | {"equals": "VALUE:hello"} | {"equals": "VALUE:hello"} |
| node-serialize IIFE marker | attack | {"equals": "LAB_NODE_EXEC"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
