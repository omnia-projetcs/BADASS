# Unrestricted upload

An attachment handler trusts a client-supplied MIME type and writes files with prohibited extensions. Inspired by EDB-45169 (CVE-2017-15580). The file writes are real; executable payloads and downstream execution are not modeled.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-434 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce the service policy on the server: permit only .txt/text/plain and .csv/text/csv pairs, validate UTF-8 text and bounded filenames, and create files exclusively. Store attachments in an owned directory without executable handlers and serve them as downloads with fixed MIME types. Filename/MIME validation is not a general malware detector; binary document formats and a web delivery layer are outside this fixture.

## Regression

```sh
python3 tools/lab.py test --case python/unrestricted-upload --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| allowed notes.txt | benign | {"equals": {"status": 201, "path": "uploads/notes.txt"}, "files": [{"path": "uploads/notes.txt", "content": "HELLO"}]} | {"equals": {"status": 201, "path": "uploads/notes.txt"}, "files": [{"path": "uploads/notes.txt", "content": "HELLO"}]} |
| allowed table.csv | benign | {"equals": {"status": 201, "path": "uploads/table.csv"}, "files": [{"path": "uploads/table.csv", "content": "name,count\nalice,2"}]} | {"equals": {"status": 201, "path": "uploads/table.csv"}, "files": [{"path": "uploads/table.csv", "content": "name,count\nalice,2"}]} |
| allowed NOTES.TXT | benign | {"equals": {"status": 201, "path": "uploads/NOTES.TXT"}, "files": [{"path": "uploads/NOTES.TXT", "content": "café"}]} | {"equals": {"status": 201, "path": "uploads/NOTES.TXT"}, "files": [{"path": "uploads/NOTES.TXT", "content": "café"}]} |
| allowed report.v2.txt | benign | {"equals": {"status": 201, "path": "uploads/report.v2.txt"}, "files": [{"path": "uploads/report.v2.txt", "content": "version 2"}]} | {"equals": {"status": 201, "path": "uploads/report.v2.txt"}, "files": [{"path": "uploads/report.v2.txt", "content": "version 2"}]} |
| spoofed MIME attachment.exe | attack | {"equals": {"status": 201, "path": "uploads/attachment.exe"}, "files": [{"path": "uploads/attachment.exe", "content": "LAB_MARKER"}]} | {"equals": {"status": 415, "error": "unsupported upload type"}, "files": [{"path": "uploads/attachment.exe", "type": "absent"}]} |
| spoofed MIME report.txt.php | attack | {"equals": {"status": 201, "path": "uploads/report.txt.php"}, "files": [{"path": "uploads/report.txt.php", "content": "LAB_MARKER"}]} | {"equals": {"status": 415, "error": "unsupported upload type"}, "files": [{"path": "uploads/report.txt.php", "type": "absent"}]} |
| spoofed MIME active.html | attack | {"equals": {"status": 201, "path": "uploads/active.html"}, "files": [{"path": "uploads/active.html", "content": "LAB_MARKER"}]} | {"equals": {"status": 415, "error": "unsupported upload type"}, "files": [{"path": "uploads/active.html", "type": "absent"}]} |
| spoofed MIME script.PHP | attack | {"equals": {"status": 201, "path": "uploads/script.PHP"}, "files": [{"path": "uploads/script.PHP", "content": "LAB_MARKER"}]} | {"equals": {"status": 415, "error": "unsupported upload type"}, "files": [{"path": "uploads/script.PHP", "type": "absent"}]} |
| mismatched text MIME | attack | {"equals": {"status": 201, "path": "uploads/notes.txt"}, "files": [{"path": "uploads/notes.txt", "content": "LAB_MARKER"}]} | {"equals": {"status": 415, "error": "unsupported upload type"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| unsupported binary MIME | benign | {"equals": {"status": 415, "error": "unsupported upload type"}} | {"equals": {"status": 415, "error": "unsupported upload type"}} |
| parent filename | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| Windows filename | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| missing fields | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| non-object | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| binary NUL content | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| non-string content | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |
| oversized content | robustness | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid upload"}, "files": [{"path": "uploads/notes.txt", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-45169 — osTicket 1.10.1 Arbitrary File Upload — r3j10r (Rajwinder Singh)](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/windows/webapps/45169.txt)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
