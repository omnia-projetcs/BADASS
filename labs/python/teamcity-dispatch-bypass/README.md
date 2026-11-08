# TeamCity: dispatch authentication bypass

An original TeamCity-inspired dispatch model authenticates the initial public path but later forwards a JSP parameter to a protected administrative handler. A successful unauthorized request commits a synthetic administrator to SQLite. This is a route-identity model, not a TeamCity server or reproduction of its Java servlet implementation.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-288 |
| CVE | CVE-2024-27198 |
| OWASP | A07:2025, API5:2023 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Resolve the effective target before authorization and enforce the administrator session on the final route, including forwards. Query parameters cannot supply a role; only the trusted session map determines access. The reduced JSP/semicolon grammar is explicit and bounded. Real TeamCity remediation is installing its patched product release.

## Regression

```sh
python3 tools/lab.py test --case python/teamcity-dispatch-bypass --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public login | benign | {"equals": {"status": 200, "page": "login"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 200, "page": "login"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| public health | benign | {"equals": {"status": 200, "health": "ok"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 200, "health": "ok"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| admin creation | benign | {"equals": {"status": 201, "created": "lab-user"}} | {"equals": {"status": 201, "created": "lab-user"}} |
| anonymous direct access denied | benign | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| reader direct access denied | benign | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| public path forwarded to admin route | attack | {"equals": {"status": 201, "created": "lab-user"}} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| missing path forwarded to admin route | attack | {"equals": {"status": 201, "created": "lab-user"}} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| reader escalates by dispatch | attack | {"equals": {"status": 201, "created": "lab-user"}} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| duplicate forward rejected | robustness | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| malformed target | robustness | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| unknown path | benign | {"equals": {"status": 404, "error": "missing route"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 404, "error": "missing route"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |
| wrong path type | robustness | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid request"}, "files": [{"path": "teamcity.sqlite", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [JetBrains TeamCity CVE-2024-27198 — official advisory](https://blog.jetbrains.com/teamcity/2024/03/additional-critical-security-issues-affecting-teamcity-on-premises-cve-2024-27198-and-cve-2024-27199-update-to-2023-11-4-now/)
- [EDB-52411 — TeamCity authentication bypass](https://www.exploit-db.com/exploits/52411)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
