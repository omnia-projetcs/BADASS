# Tenant export worker

Export enqueueing validates tenant ownership and persists trusted scope, but a separate worker connection queries SQLite by document ID alone. Identical local IDs in different tenants then cause an export of another tenant's data. EDB-41433 motivates unauthorized client export; the queue mechanism is an original extension.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-863 |
| OWASP | A01:2025, API1:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Carry the authenticated tenant in the service-owned job and constrain the worker query by both tenant and document ID. The composite database key is (tenant,id). Tests inspect the serialized job, real SQLite rows and exported bytes. The queue is replayed synchronously in an owned temporary directory; broker authentication, permission revocation and scheduling races are outside this fixture.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-export-worker --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| north local ID | benign | {"equals": {"status": 200, "content": "LAB_NORTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_NORTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"north\"}\n"}]} | {"equals": {"status": 200, "content": "LAB_NORTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_NORTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"north\"}\n"}]} |
| south distinct ID | benign | {"equals": {"status": 200, "content": "LAB_SOUTH_SECOND_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_SOUTH_SECOND_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 2, \"tenant\": \"south\"}\n"}]} | {"equals": {"status": 200, "content": "LAB_SOUTH_SECOND_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_SOUTH_SECOND_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 2, \"tenant\": \"south\"}\n"}]} |
| colliding local ID | attack | {"equals": {"status": 200, "content": "LAB_NORTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_NORTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"south\"}\n"}]} | {"equals": {"status": 200, "content": "LAB_SOUTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_SOUTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"south\"}\n"}]} |
| client tenant is ignored | attack | {"equals": {"status": 200, "content": "LAB_NORTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_NORTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"south\"}\n"}]} | {"equals": {"status": 200, "content": "LAB_SOUTH_EXPORT"}, "files": [{"path": "export.txt", "content": "LAB_SOUTH_EXPORT"}, {"path": "queued-job.json", "content": "{\"document_id\": 1, \"tenant\": \"south\"}\n"}]} |
| foreign-only ID cannot be queued | benign | {"equals": {"status": 404}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 404}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |
| missing document | benign | {"equals": {"status": 404}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 404}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |
| invalid session | benign | {"equals": {"status": 401}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 401}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |
| string ID | robustness | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |
| boolean ID | robustness | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |
| non-object request | robustness | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "export.txt", "type": "absent"}, {"path": "queued-job.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-41433 — ProjectSend r754 client export IDOR — Lawrence Amer](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/41433.txt)
- [OWASP API1:2023 — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
