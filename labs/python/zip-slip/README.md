# Zip slip

An archive member filename escapes the uploads directory during a real ZIP extraction and overwrites a synthetic sibling file. Inspired by EDB-39816 (CVE-2016-4313); original Python code models the extraction defect, not eXtplorer itself.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-22 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate all member destinations before extraction: reject absolute paths, Windows drives, parent segments, duplicate destinations and resolved symlink escapes. Allow nested relative filenames only within uploads. The fixture builds bounded regular-file ZIP members from JSON and assumes an owned temporary directory without concurrent writers; it does not model arbitrary compressed uploads or extraction races.

## Regression

```sh
python3 tools/lab.py test --case python/zip-slip --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| regular file | benign | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "uploads/hello.txt", "content": "HELLO"}]} | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "uploads/hello.txt", "content": "HELLO"}]} |
| nested regular file | benign | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "uploads/docs/readme.txt", "content": "GUIDE"}]} | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "uploads/docs/readme.txt", "content": "GUIDE"}]} |
| parent overwrite | attack | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "secret.txt", "content": "LAB_OVERWRITTEN"}]} | {"equals": {"status": 400, "error": "unsafe archive path"}, "files": [{"path": "secret.txt", "content": "LAB_SECRET"}]} |
| Windows separator overwrite | attack | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "secret.txt", "content": "LAB_OVERWRITTEN"}]} | {"equals": {"status": 400, "error": "unsafe archive path"}, "files": [{"path": "secret.txt", "content": "LAB_SECRET"}]} |
| sibling prefix escape | attack | {"equals": {"status": 200, "extracted": 1}, "files": [{"path": "uploads-other/marker.txt", "content": "MARKER"}]} | {"equals": {"status": 400, "error": "unsafe archive path"}, "files": [{"path": "uploads-other/marker.txt", "type": "absent"}]} |
| validate whole archive before writing | attack | {"equals": {"status": 200, "extracted": 2}, "files": [{"path": "uploads/hello.txt", "content": "HELLO"}, {"path": "secret.txt", "content": "LAB_OVERWRITTEN"}]} | {"equals": {"status": 400, "error": "unsafe archive path"}, "files": [{"path": "uploads/hello.txt", "type": "absent"}, {"path": "secret.txt", "content": "LAB_SECRET"}]} |
| wrong input type | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| empty archive | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| missing member name | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| NUL member | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| oversized member | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |
| non-string content | robustness | {"equals": {"status": 400, "error": "invalid archive"}} | {"equals": {"status": 400, "error": "invalid archive"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-39816 — eXtplorer 2.1.9 — ZIP Directory Traversal (hyp3rlinx, 2016-05-16)](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/39816.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
