# FortiOS: forwarded-header authentication bypass

Original reduced Python model inspired by CVE-2022-40684. An appliance handler trusts a loopback identity claimed in client Forwarded and User-Agent headers. A forged request writes a synthetic administrator key marker to a real local file. No Fortinet code, SSH key or SSH login is involved.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-288 |
| CVE | CVE-2022-40684 |
| OWASP | A07:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require an issued administrator token independent of client forwarding headers. Normalize header names and reject case-colliding duplicates before authorization. Real deployments must also authenticate trusted proxy or internal-service channels; this fixture models only the external request boundary.

## Regression

```sh
python3 tools/lab.py test --case python/fortios-forwarded-auth --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid admin token | benign | {"equals": {"status": 200, "key": "LAB_KEY_ADMIN"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_ADMIN\n"}]} | {"equals": {"status": 200, "key": "LAB_KEY_ADMIN"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_ADMIN\n"}]} |
| lowercase header token | benign | {"equals": {"status": 200, "key": "LAB_KEY_ADMIN"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_ADMIN\n"}]} | {"equals": {"status": 200, "key": "LAB_KEY_ADMIN"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_ADMIN\n"}]} |
| anonymous request | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| forged internal identity | attack | {"equals": {"status": 200, "key": "LAB_KEY_NEW"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_NEW\n"}]} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "appliance-admin.keys", "type": "absent"}]} |
| alternate trusted agent spoof | attack | {"equals": {"status": 200, "key": "LAB_KEY_OTHER"}, "files": [{"path": "appliance-admin.keys", "content": "LAB_KEY_OTHER\n"}]} | {"equals": {"status": 401, "error": "denied"}} |
| user agent alone denied | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| colliding authorization fields | robustness | {"equals": {"status": 400, "error": "invalid key request"}} | {"equals": {"status": 400, "error": "invalid key request"}} |
| bad key shape | robustness | {"equals": {"status": 400, "error": "invalid key request"}} | {"equals": {"status": 400, "error": "invalid key request"}} |
| header injection rejected | robustness | {"equals": {"status": 400, "error": "invalid key request"}} | {"equals": {"status": 400, "error": "invalid key request"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Fortinet CVE-2022-40684 — vendor advisory](https://www.fortiguard.com/psirt/FG-IR-22-377)
- [EDB-51092 — Fortinet forwarded-header authentication bypass](https://www.exploit-db.com/exploits/51092)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
