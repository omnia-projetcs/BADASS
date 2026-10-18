# Tenant and privilege isolation

These seven paired REST API handler fixtures exercise different boundaries between
organizations, authenticated sessions and tenant-scoped administrative roles.
They run locally with Python's standard library and synthetic data. No HTTP
server, external account or queue broker is required.

| Case | Vulnerable behavior | Required isolation |
|---|---|---|
| [Shared cache](../labs/rest-api/tenant-cache/README.md) | A cache hit returns the previous organization's document. | Scope the cache key to the authenticated tenant and local document ID. |
| [Tenant administrator](../labs/rest-api/tenant-admin-scope/README.md) | An administrator in one organization disables a user in another. | Check the admin membership in the target user's actual organization. |
| [Export worker](../labs/rest-api/tenant-export-worker/README.md) | The enqueue check is correct, but the worker drops tenant scope from its query. | Retain the authenticated tenant through serialization and data access. |
| [Batch mutation](../labs/rest-api/tenant-bulk-update/README.md) | An authorized first ID permits changes to foreign IDs later in the batch. | Authorize every object and reject mixed batches before any write. |
| [Signed download](../labs/rest-api/tenant-signed-download/README.md) | A valid signature can be reused with another tenant because the tenant was not signed. | Authenticate the complete resource tuple, action and expiration. |
| [Session switch](../labs/rest-api/tenant-session-switch/README.md) | Switching organizations keeps the previous organization's admin role. | Change the active tenant and its role together from trusted memberships. |
| [Storage prefix](../labs/rest-api/tenant-storage-prefix/README.md) | The path prefix for `north` also matches the sibling `north-backup` directory. | Check resolved path ancestry within the authenticated tenant root. |

## Run the cases

From the repository root:

```sh
python3 tools/lab.py test --case rest-api/tenant-cache --strict
python3 tools/lab.py test --case rest-api/tenant-admin-scope --strict
python3 tools/lab.py test --case rest-api/tenant-export-worker --strict
python3 tools/lab.py test --case rest-api/tenant-bulk-update --strict
python3 tools/lab.py test --case rest-api/tenant-signed-download --strict
python3 tools/lab.py test --case rest-api/tenant-session-switch --strict
python3 tools/lab.py test --case rest-api/tenant-storage-prefix --strict
python3 -m unittest discover -s tests -p test_tenant_isolation.py -v
python3 -m unittest discover -s tests -p test_tenant_capabilities.py -v
```

## Trusted context and observations

Sessions resolve through service-owned tables. Fields named `tenant`, `tenant_id`
or `role` in a request cannot expand the authenticated caller's scope. The
administrator case deliberately gives one caller an admin membership in north
and a viewer membership in south, making global-role mistakes observable.

The cache test runs successive requests against the same cache in both tenant
orders. The worker persists a job and opens a separate SQLite connection; its
documents have a composite `(tenant,id)` key. The batch case uses a real SQLite
transaction. Tests inspect the serialized job, exported bytes, account snapshots
and committed database rows independently of response status codes. Rejected
mixed batches must change neither authorized nor foreign rows.

The download case issues a bearer grant with a fresh random HMAC key and then
redeems it, demonstrating that a valid signature must cover the full tenant and
document identity. Independent tests recompute the MAC and reject modified keys,
document IDs, expiry values and expired grants. The session case records both
the updated authorization context and the accounts affected by later actions.
Storage tests read actual sibling files and exercise resolved symlink targets.

## Scope

These are application-level models. The worker is executed synchronously after
serialization, and the queue files are service-owned. The cases do not certify
broker access controls, distributed cache invalidation, revocation during job
execution, database row-level security or OS/container isolation. The cache
policy shares documents within each tenant; private per-user documents would
require additional authorization dimensions.

Signed downloads are intentionally shareable within the exact granted resource
and use a pinned laboratory clock. The session model is sequential; it does not
model concurrent membership changes. Path ancestry checks assume no concurrent
replacement of the trusted storage tree. These additions follow the boundaries
discussed in the [OWASP multi-tenant security guidance](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html).

The export and mutation cases adapt the authorization failure patterns described
in [EDB-41433](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/41433.txt)
and [EDB-39473](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/39473.txt).
Their queue and tenant mechanisms are original laboratory extensions, not
reproductions of those products. Cache and role boundaries are documented with
MITRE CWE-488 and OWASP API1/API5 references in the individual case READMEs.
