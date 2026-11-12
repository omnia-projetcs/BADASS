# NoSQL operator injection

A document query handler evaluates nested operator objects such as $ne in authentication fields, bypassing secret verification.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-943 |
| OWASP | A05:2025, API8:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject non-scalar query parameters, require strict ASCII string types, and compare secrets in constant time.

## Regression

```sh
python3 tools/lab.py test --case rest-api/nosql-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid scalar credentials | benign | {"equals": {"authenticated": "alice", "role": "admin"}} | {"equals": {"authenticated": "alice", "role": "admin"}} |
| operator injection $ne | attack | {"equals": {"authenticated": "alice", "role": "admin"}} | {"equals": "DENIED"} |
| operator injection $gt | attack | {"equals": {"authenticated": "alice", "role": "admin"}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
