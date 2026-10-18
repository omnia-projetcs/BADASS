# Tenant storage prefix

A storage handler resolves a requested path and checks that its string starts with the tenant root. The sibling directory north-backup passes the north prefix test, allowing another tenant's private file to be read. The regression reads actual UTF-8 files.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-22 |
| OWASP | A01:2025, API1:2023 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Compare resolved path ancestry, not textual prefixes, and obtain the storage root from the authenticated session. Preserve valid nested and normalized in-root paths. This fixture assumes an owned local directory tree without concurrent symlink replacement; it does not claim race-free OS sandboxing.

## Regression

```sh
python3 tools/lab.py test --case rest-api/tenant-storage-prefix --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| own report | benign | {"equals": {"status": 200, "content": "LAB_NORTH_STORAGE"}} | {"equals": {"status": 200, "content": "LAB_NORTH_STORAGE"}} |
| nested own document | benign | {"equals": {"status": 200, "content": "LAB_NORTH_NOTES"}} | {"equals": {"status": 200, "content": "LAB_NORTH_NOTES"}} |
| normalized own path | benign | {"equals": {"status": 200, "content": "LAB_NORTH_STORAGE"}} | {"equals": {"status": 200, "content": "LAB_NORTH_STORAGE"}} |
| backup tenant own document | benign | {"equals": {"status": 200, "content": "LAB_BACKUP_PRIVATE"}} | {"equals": {"status": 200, "content": "LAB_BACKUP_PRIVATE"}} |
| south tenant own document | benign | {"equals": {"status": 200, "content": "LAB_SOUTH_PRIVATE"}} | {"equals": {"status": 200, "content": "LAB_SOUTH_PRIVATE"}} |
| sibling prefix escape | attack | {"equals": {"status": 200, "content": "LAB_BACKUP_PRIVATE"}} | {"equals": {"status": 403}} |
| nested sibling prefix escape | attack | {"equals": {"status": 200, "content": "LAB_BACKUP_PRIVATE"}} | {"equals": {"status": 403}} |
| body tenant cannot choose root | attack | {"equals": {"status": 200, "content": "LAB_BACKUP_PRIVATE"}} | {"equals": {"status": 403}} |
| unrelated sibling denied | benign | {"equals": {"status": 403}} | {"equals": {"status": 403}} |
| parent directory denied | benign | {"equals": {"status": 403}} | {"equals": {"status": 403}} |
| missing file | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| directory not a file | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| invalid session | benign | {"equals": {"status": 401}} | {"equals": {"status": 401}} |
| non-object request | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| non-string path | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| empty path | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| NUL path | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| oversized path | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [OWASP — Multi-Tenant Application Security](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
- [MITRE CWE-187 — Partial String Comparison](https://cwe.mitre.org/data/definitions/187.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
