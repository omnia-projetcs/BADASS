# Factory authentication bypass

A factoryBypass query parameter creates an administrator session without credentials. A successful request updates a real SQLite configuration row, making the unauthorized state change observable. Inspired by EDB-40156; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-288 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Remove the factory bypass from the remote request path and require an existing server-side administrator session. Session tokens are fixed synthetic credentials in this fixture, not a production session scheme. Tests inspect committed sessions and configuration rows; other weaknesses in the multi-issue EDB report are outside this case.

## Regression

```sh
python3 tools/lab.py test --case python/factory-auth-bypass --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| administrator update | benign | {"equals": {"status": 200, "banner": "HELLO"}} | {"equals": {"status": 200, "banner": "HELLO"}} |
| anonymous denied | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| reader denied | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| factory parameter grants admin | attack | {"equals": {"status": 200, "banner": "CHANGED"}} | {"equals": {"status": 401, "error": "denied"}} |
| presence bypass with zero | attack | {"equals": {"status": 200, "banner": "CHANGED"}} | {"equals": {"status": 401, "error": "denied"}} |
| reader escalates through factory path | attack | {"equals": {"status": 200, "banner": "CHANGED"}} | {"equals": {"status": 401, "error": "denied"}} |
| unrelated query has no bypass | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| missing banner | robustness | {"equals": {"status": 400, "error": "invalid request"}} | {"equals": {"status": 400, "error": "invalid request"}} |
| wrong query type | robustness | {"equals": {"status": 400, "error": "invalid request"}} | {"equals": {"status": 400, "error": "invalid request"}} |
| wrong request type | robustness | {"equals": {"status": 400, "error": "invalid request"}} | {"equals": {"status": 400, "error": "invalid request"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-40156 — Ubee EVW3226 1.0.20 — factoryBypass authentication bypass (Gergely Eberhardt)](https://www.exploit-db.com/exploits/40156)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
