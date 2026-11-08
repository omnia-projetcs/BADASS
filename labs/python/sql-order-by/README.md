# SQL injection in an ORDER BY identifier

A client sorting expression reaches an SQLite ORDER BY clause and can query private data through result ordering.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-89 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Map public sorting choices to constant application-owned SQL column names; value placeholders do not bind identifiers.

## Regression

```sh
python3 tools/lab.py test --case python/sql-order-by --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| sort by name | benign | {"equals": {"status": 200, "rows": ["alpha", "beta", "gamma"]}} | {"equals": {"status": 200, "rows": ["alpha", "beta", "gamma"]}} |
| sort by price | benign | {"equals": {"status": 200, "rows": ["beta", "gamma", "alpha"]}} | {"equals": {"status": 200, "rows": ["beta", "gamma", "alpha"]}} |
| unauthorized direction expression | attack | {"equals": {"status": 200, "rows": ["gamma", "beta", "alpha"]}} | {"equals": {"status": 400, "error": "invalid sort"}} |
| private value controls ascending order | attack | {"equals": {"status": 200, "rows": ["beta", "gamma", "alpha"]}} | {"equals": {"status": 400, "error": "invalid sort"}} |
| wrong private guess reverses ordering | attack | {"equals": {"status": 200, "rows": ["alpha", "gamma", "beta"]}} | {"equals": {"status": 400, "error": "invalid sort"}} |
| sort must be a string | robustness | {"equals": {"status": 400, "error": "invalid sort"}} | {"equals": {"status": 400, "error": "invalid sort"}} |
| missing sort field | robustness | {"equals": {"status": 400, "error": "invalid sort"}} | {"equals": {"status": 400, "error": "invalid sort"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
