# Tenant admin scope

A user who is an administrator in north but only a viewer in south can disable a south account because authorization searches for any admin membership. The target account's tenant and the caller's memberships are server-owned.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-863 |
| OWASP | A01:2025, API5:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Resolve administrative authority in the target account's actual tenant. A tenant administrator has no platform-wide privilege. Ignore client-supplied tenant and role fields, and leave all accounts unchanged when authorization fails. The persisted JSON file is an observation of this bounded local mutation, not a concurrent account service.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-admin-scope --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| north admin own tenant | benign | {"equals": {"status": 200, "disabled": "north-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 200, "disabled": "north-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| south admin own tenant | benign | {"equals": {"status": 200, "disabled": "south-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 200, "disabled": "south-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}\n"}]} |
| viewer cannot disable | benign | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| admin elsewhere but viewer here | attack | {"equals": {"status": 200, "disabled": "south-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| admin without target membership | attack | {"equals": {"status": 200, "disabled": "north-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| forged tenant and role | attack | {"equals": {"status": 200, "disabled": "south-member"}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| viewer cannot claim admin | benign | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 403}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| invalid session | benign | {"equals": {"status": 401}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 401}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| unknown account | benign | {"equals": {"status": 404}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 404}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |
| non-string account | robustness | {"equals": {"status": 400}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "accounts-state.json", "content": "{\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}\n"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [OWASP API5:2023 — Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
