# GraphQL depth amplification and introspection

An unbounded GraphQL resolver executes deeply nested cyclic selections and exposes internal schema introspection.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-400, CWE-200 |
| OWASP | API4:2023, A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce a strict maximum query depth, allowlist public fields, and reject __schema and __type introspection queries.

## Regression

```sh
python3 tools/lab.py test --case rest-api/graphql-depth-amplification --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| shallow profile query | benign | {"equals": {"org": {"name": "alice", "depth": 2}}} | {"equals": {"org": {"name": "alice", "depth": 2}}} |
| cyclic depth bomb | attack | {"equals": {"org": {"members": {"org": {"members": {"name": "alice", "depth": 5}}}}}} | {"equals": "DENIED"} |
| schema introspection query | attack | {"equals": {"types": ["Query", "User", "Organization", "InternalSecret"], "depth": 1}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
