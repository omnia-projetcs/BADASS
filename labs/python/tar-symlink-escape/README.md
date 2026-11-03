# TAR symlink escape

An upload constructs and parses a real in-memory TAR archive. Lexically valid member names can follow an earlier archive symlink to overwrite a synthetic file outside unpacked/. Inspired by EDB-43002; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-59 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Preflight every parsed TAR member, accept regular files only, reject symlinks in destination parents and enforce resolved containment before extraction. The local harness confines even the vulnerable link targets to its working directory. No Documentum code is included; concurrent filesystem mutation and hard-link extraction are outside this bounded fixture.

## Regression

```sh
python3 tools/lab.py test --case python/tar-symlink-escape --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| regular file | benign | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "unpacked/readme.txt", "content": "HELLO"}]} | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "unpacked/readme.txt", "content": "HELLO"}]} |
| nested file | benign | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "unpacked/docs/notes.txt", "content": "NOTES"}]} | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "unpacked/docs/notes.txt", "content": "NOTES"}]} |
| link redirects write | attack | {"equals": {"status": 200, "extracted": 2}, "files": [{"path": "secret.txt", "content": "LAB_OVERWRITTEN"}]} | {"equals": {"status": 400, "error": "unsafe archive member"}, "files": [{"path": "secret.txt", "content": "LAB_SECRET"}, {"path": "unpacked/pivot", "type": "absent"}]} |
| preflight before writing | attack | {"equals": {"status": 200, "extracted": 3}, "files": [{"path": "unpacked/readme.txt", "content": "HELLO"}, {"path": "private.txt", "content": "CHANGED"}]} | {"equals": {"status": 400, "error": "unsafe archive member"}, "files": [{"path": "unpacked/readme.txt", "type": "absent"}, {"path": "private.txt", "content": "LAB_SECRET"}]} |
| plain traversal rejected | benign | {"equals": {"status": 400, "error": "unsafe archive member"}} | {"equals": {"status": 400, "error": "unsafe archive member"}} |
| duplicate member rejected | benign | {"equals": {"status": 400, "error": "unsafe archive member"}} | {"equals": {"status": 400, "error": "unsafe archive member"}} |
| empty archive | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| invalid content | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| NUL name | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| oversized content | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-43002 — OpenText Documentum Content Server — TAR symlink traversal / CVE-2017-15276 (Andrey B. Panfilov)](https://www.exploit-db.com/exploits/43002)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
