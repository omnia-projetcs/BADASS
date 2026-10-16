# SQL injection

A model-supplied database-tool argument is concatenated into SQL and changes the query structure.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-89  
**OWASP:** A05:2025, LLM05:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep SQL structure constant and bind the untrusted value as a parameter. Execute against a fresh in-memory SQLite database.

## Regression

```sh
python3 tools/lab.py test --case ai/sql-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| existing account | benign | {"equals": ["alice"]} | {"equals": ["alice"]} |
| missing account | benign | {"equals": []} | {"equals": []} |
| empty value | benign | {"equals": []} | {"equals": []} |
| ordinary SQL-looking text | benign | {"equals": []} | {"equals": []} |
| tautology with comment | attack | {"equals": ["alice", "admin"]} | {"equals": []} |
| targeted account bypass | attack | {"equals": ["admin"]} | {"equals": []} |
| UNION injected row | attack | {"equals": ["LAB_UNION"]} | {"equals": []} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
