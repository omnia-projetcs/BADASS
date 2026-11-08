# Second-order SQL injection

A search value is committed safely to SQLite, read through a new connection, then concatenated into a later query.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-89 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Keep persisted client values untrusted and bind them at every SQL execution boundary, including later report queries.

## Regression

```sh
python3 tools/lab.py test --case python/sql-second-order --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| existing name | benign | {"equals": {"status": 200, "stored": "alice", "matches": ["alice"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "alice", "matches": ["alice"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| second existing name | benign | {"equals": {"status": 200, "stored": "bob", "matches": ["bob"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "bob", "matches": ["bob"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| unknown name | benign | {"equals": {"status": 200, "stored": "unknown", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "unknown", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| empty saved name | benign | {"equals": {"status": 200, "stored": "", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| persisted predicate bypass | attack | {"equals": {"status": 200, "stored": "' OR 1=1 --", "matches": ["alice", "bob"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "' OR 1=1 --", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| persisted UNION private row | attack | {"equals": {"status": 200, "stored": "' UNION SELECT value FROM internal --", "matches": ["LAB_SECOND_ORDER_SECRET"]}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "' UNION SELECT value FROM internal --", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| literal apostrophe remains data | functional | {"equals": {"status": 400, "error": "invalid saved query"}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} | {"equals": {"status": 200, "stored": "O'Reilly", "matches": []}, "files": [{"path": "saved-search.sqlite", "type": "file"}]} |
| name must be a string | robustness | {"equals": {"status": 400, "error": "invalid name"}, "files": [{"path": "saved-search.sqlite", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid name"}, "files": [{"path": "saved-search.sqlite", "type": "absent"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
