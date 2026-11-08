# Sql login bypass

SQL concatenation lets a login name remove the password predicate and authenticate as a synthetic administrator. Inspired by EDB-41029; this is an original Python model, not the affected PHP product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-89 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Bind username and password key as SQLite parameters. The in-memory fixture uses known test accounts and a fixed PBKDF2 salt only for deterministic demonstration; it is not a production authentication system.

## Regression

```sh
python3 tools/lab.py test --case python/sql-login-bypass --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid administrator | benign | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 200, "user": "admin", "role": "admin"}} |
| valid reader | benign | {"equals": {"status": 200, "user": "alice", "role": "reader"}} | {"equals": {"status": 200, "user": "alice", "role": "reader"}} |
| wrong password | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| unknown username | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| comment removes password check | attack | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 401, "error": "denied"}} |
| tautology bypass | attack | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 401, "error": "denied"}} |
| union fabricates authenticated identity | attack | {"equals": {"status": 200, "user": "forged", "role": "admin"}} | {"equals": {"status": 401, "error": "denied"}} |
| literal apostrophe account | functional | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 200, "user": "O'Reilly", "role": "reader"}} |
| missing credentials | robustness | {"equals": {"status": 400, "error": "invalid credentials"}} | {"equals": {"status": 400, "error": "invalid credentials"}} |
| wrong input type | robustness | {"equals": {"status": 400, "error": "invalid credentials"}} | {"equals": {"status": 400, "error": "invalid credentials"}} |
| non-string password | robustness | {"equals": {"status": 400, "error": "invalid credentials"}} | {"equals": {"status": 400, "error": "invalid credentials"}} |
| NUL username | robustness | {"equals": {"status": 400, "error": "invalid credentials"}} | {"equals": {"status": 400, "error": "invalid credentials"}} |
| oversized username | robustness | {"equals": {"status": 400, "error": "invalid credentials"}} | {"equals": {"status": 400, "error": "invalid credentials"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-41029 — Online Food Delivery 2.04 — Authentication Bypass (Dawid Morawski, 2017-01-12)](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/41029.txt)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
