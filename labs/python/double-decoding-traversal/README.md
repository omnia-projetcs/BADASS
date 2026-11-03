# Double-decoding path traversal

A download handler checks the first URL decoding pass but reads a path after a second pass. Nested percent encodings can disclose a real synthetic file outside public/. Inspired by EDB-50406; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-22 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Decode to a bounded stable form before validation, reject residual encodings and backslashes, then resolve and enforce containment in public/. Reads use real local files. The model covers disclosure only, not Apache CGI execution; concurrent filesystem mutation is outside this fixture.

## Regression

```sh
python3 tools/lab.py test --case python/double-decoding-traversal --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public file | benign | {"equals": {"status": 200, "body": "WELCOME"}} | {"equals": {"status": 200, "body": "WELCOME"}} |
| encoded public name | benign | {"equals": {"status": 200, "body": "WELCOME"}} | {"equals": {"status": 200, "body": "WELCOME"}} |
| missing file | benign | {"equals": {"status": 404, "error": "missing file"}} | {"equals": {"status": 404, "error": "missing file"}} |
| plain traversal denied | benign | {"equals": {"status": 403, "error": "outside public root"}} | {"equals": {"status": 403, "error": "outside public root"}} |
| double encoded traversal | attack | {"equals": {"status": 200, "body": "LAB_SECRET"}} | {"equals": {"status": 403, "error": "outside public root"}} |
| mixed encoded dots | attack | {"equals": {"status": 200, "body": "LAB_SECRET"}} | {"equals": {"status": 403, "error": "outside public root"}} |
| wrong type | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |
| malformed UTF8 | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |
| encoded NUL | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-50406 — Apache HTTP Server 2.4.50 — Path Traversal / CVE-2021-42013 (Lucas Souza)](https://www.exploit-db.com/exploits/50406)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
