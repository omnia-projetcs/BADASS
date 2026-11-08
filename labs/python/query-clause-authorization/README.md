# Query-clause authorization bypass

A query gateway checks restricted-table permissions only on its simple query branch. Adding an allowed WHERE or ORDER BY clause lets a reader retrieve private role rows from real SQLite queries. Inspired by EDB-44068; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-863 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Authorize the resolved table before branching on query clauses. Table and sort identifiers are mapped from allowlists and filter values are bound as parameters in both variants, isolating the authorization weakness from SQL injection. Trusted fixture tokens determine roles; only the metadata-disclosure stage of the OrientDB report is modeled, not its later code-execution chain.

## Regression

```sh
python3 tools/lab.py test --case python/query-clause-authorization --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| reader public table | benign | {"equals": {"status": 200, "rows": ["public"]}} | {"equals": {"status": 200, "rows": ["public"]}} |
| reader public sorted table | benign | {"equals": {"status": 200, "rows": ["public"]}} | {"equals": {"status": 200, "rows": ["public"]}} |
| admin private table | benign | {"equals": {"status": 200, "rows": ["admin", "reader"]}} | {"equals": {"status": 200, "rows": ["admin", "reader"]}} |
| plain restricted query denied | benign | {"equals": {"status": 403, "error": "restricted table"}} | {"equals": {"status": 403, "error": "restricted table"}} |
| ORDER BY bypass | attack | {"equals": {"status": 200, "rows": ["admin", "reader"]}} | {"equals": {"status": 403, "error": "restricted table"}} |
| WHERE bypass | attack | {"equals": {"status": 200, "rows": ["admin"]}} | {"equals": {"status": 403, "error": "restricted table"}} |
| descending bypass | attack | {"equals": {"status": 200, "rows": ["reader", "admin"]}} | {"equals": {"status": 403, "error": "restricted table"}} |
| filter binds SQL characters | benign | {"equals": {"status": 200, "rows": []}} | {"equals": {"status": 200, "rows": []}} |
| sort identifier injection denied | robustness | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 400, "error": "invalid query"}} |
| wrong table type | robustness | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 400, "error": "invalid query"}} |
| unknown token | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-44068 — OrientDB — query-clause permission bypass / CVE-2017-11467 (SecuriTeam / Francis Alexander)](https://www.exploit-db.com/exploits/44068)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
