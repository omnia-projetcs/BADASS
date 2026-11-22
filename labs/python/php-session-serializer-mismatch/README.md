# PHP: upload-progress session serializer mismatch

An original Python handler model of PHP session serializer mismatch during upload progress. Writing an attacker-controlled key in php_serialize-style framing and reading it back with the pipe-delimited php serializer lets a '|' delimiter split the entry and instantiate an unintended object. No PHP runtime is embedded.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-436, CWE-502 |
| CVE | CVE-2026-115560 |
| OWASP | A06:2025, A08:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use a single structured serializer (such as JSON) across both upload-progress writes and session reads, validate upload key characters, and never instantiate arbitrary objects from session storage. Real PHP deployments require upgrading to PHP 8.2.36, 8.3.37, 8.4.28, 8.5.13 or 8.6.0.

## Regression

```sh
python3 tools/lab.py test --case python/php-session-serializer-mismatch --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal upload progress key | benign | {"equals": {"status": 200, "values": {"upload_avatar_1": "done"}, "objects": []}} | {"equals": {"status": 200, "values": {"upload_avatar_1": "done"}, "objects": []}} |
| pipe delimiter injects serialized object | attack | {"equals": {"status": 200, "values": {}, "objects": ["Runner"]}, "files": [{"path": "deserialized-object.txt", "content": "Runner\n"}]} | {"equals": {"status": 400, "error": "invalid upload key"}, "files": [{"path": "deserialized-object.txt", "type": "absent"}]} |
| missing upload key | robustness | {"equals": {"status": 400, "error": "invalid session payload"}} | {"equals": {"status": 400, "error": "invalid session payload"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2026-115560 — session upload-progress serializer mismatch](https://www.php.net/archive/2026.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
