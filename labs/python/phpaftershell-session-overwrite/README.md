# phpAfterShell: non-atomic session overwrite

An original Python handler model of phpAfterShell. Updating a file-based session in place without truncating or atomically replacing the file leaves old trailing bytes when a write is interrupted. Subsequent session parsing interprets the hybrid payload as a serialized object. No PHP runtime or gadget chain is embedded.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-367, CWE-502 |
| CVE | CVE-2026-126714 |
| OWASP | A06:2025, A08:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Write updated session data to a temporary file and atomically replace the target on completion, aborting partial writes cleanly, and reject serialized object tags during session decoding. Real PHP deployments require upgrading to PHP 8.2.36, 8.3.37, 8.4.28, 8.5.13 or 8.6.0.

## Regression

```sh
python3 tools/lab.py test --case python/phpaftershell-session-overwrite --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| complete session update | benign | {"equals": {"status": 200, "values": {"note": "fresh"}, "objects": []}} | {"equals": {"status": 200, "values": {"note": "fresh"}, "objects": []}} |
| interrupted overwrite leaves hybrid object tail | attack | {"equals": {"status": 200, "values": {"note": "new"}, "objects": ["Runner"]}, "files": [{"path": "gadget-ran.txt", "content": "Runner\n"}]} | {"equals": {"status": 409, "error": "interrupted session write"}, "files": [{"path": "gadget-ran.txt", "type": "absent"}]} |
| malformed payload shape | robustness | {"equals": {"status": 400, "error": "invalid session operation"}} | {"equals": {"status": 400, "error": "invalid session operation"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2026-126714 — phpAfterShell session file overwrite](https://www.php.net/archive/2026.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
