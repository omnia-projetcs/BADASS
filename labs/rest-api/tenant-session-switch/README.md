# Tenant session switch

A session caches both tenant and role. Switching to an allowed organization changes only the tenant, so a former administrator remains privileged in an organization where the same user is merely a viewer. Conversely, stale viewer privileges can block a valid admin operation after switching.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-863 |
| OWASP | A01:2025, API5:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Recompute the role from service-owned memberships whenever the active tenant changes. Update tenant and role together, reject non-member destinations without altering the session, and check target ownership during administrative actions. Tests inspect the resulting session and account snapshot. Membership revocation during concurrent requests is not modeled.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-session-switch --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| admin in initial tenant | benign | {"equals": {"events": [{"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| viewer in initial tenant | benign | {"equals": {"events": [{"status": 403}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"viewer\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} | {"equals": {"events": [{"status": 403}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"viewer\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} |
| same tenant switch | benign | {"equals": {"events": [{"status": 200, "tenant": "north"}, {"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 200, "tenant": "north"}, {"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| admin role survives downgrade | attack | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 200, "disabled": "south-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 403}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"viewer\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} |
| body role cannot preserve privilege | attack | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 200, "disabled": "south-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 403}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"viewer\", \"subject\": \"alice\", \"tenant\": \"south\"}}\n"}]} |
| legitimate role upgrade | functional | {"equals": {"events": [{"status": 200, "tenant": "north"}, {"status": 403}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"viewer\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 200, "tenant": "north"}, {"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| switch back after denied action | attack | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 200, "disabled": "south-member"}, {"status": 200, "tenant": "north"}, {"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 200, "tenant": "south"}, {"status": 403}, {"status": 200, "tenant": "north"}, {"status": 200, "disabled": "north-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": false, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| non-member switch preserves session | benign | {"equals": {"events": [{"status": 403}, {"status": 200, "disabled": "south-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"bob\", \"tenant\": \"south\"}}\n"}]} | {"equals": {"events": [{"status": 403}, {"status": 200, "disabled": "south-member"}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": false, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"bob\", \"tenant\": \"south\"}}\n"}]} |
| target tenant still checked | benign | {"equals": {"events": [{"status": 404}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 404}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| invalid action shape | robustness | {"equals": {"events": [{"status": 400}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 400}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| invalid switch tenant | robustness | {"equals": {"events": [{"status": 400}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} | {"equals": {"events": [{"status": 400}]}, "files": [{"path": "session-state.json", "content": "{\"accounts\": {\"north-member\": {\"active\": true, \"tenant\": \"north\"}, \"south-member\": {\"active\": true, \"tenant\": \"south\"}}, \"session\": {\"role\": \"admin\", \"subject\": \"alice\", \"tenant\": \"north\"}}\n"}]} |
| invalid session | robustness | {"equals": {"status": 401}, "files": [{"path": "session-state.json", "type": "absent"}]} | {"equals": {"status": 401}, "files": [{"path": "session-state.json", "type": "absent"}]} |
| empty actions | robustness | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} |
| oversized actions | robustness | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} |
| non-object request | robustness | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "session-state.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [OWASP — Multi-Tenant Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
