# Remote-file import SSRF

An authenticated remote-file import accepts internal destinations and writes returned synthetic content into actual download files. URL parsing, address resolution and endpoint fetching are separate operations. Inspired by EDB-51030; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-918 |
| OWASP | A01:2025, API7:2023 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Preflight every URL and all resolved addresses, reject non-global destinations, and pass the validated address to the offline fetch dependency. Invalid mixed batches produce no files. This handler model uses a fixed trusted DNS/endpoint registry, never external DNS or HTTP; it does not model redirects, proxies, TLS or CVAT task processing.

## Regression

```sh
python3 tools/lab.py test --case python/remote-import-ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public import | benign | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}]} | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}]} |
| public literal | benign | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}]} | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}]} |
| loopback import | attack | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "LAB_INTERNAL_CONFIG"}]} | {"equals": {"status": 403, "error": "internal destination"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| private DNS import | attack | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "LAB_INTERNAL_CONFIG"}]} | {"equals": {"status": 403, "error": "internal destination"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| IPv6 loopback | attack | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "LAB_INTERNAL_CONFIG"}]} | {"equals": {"status": 403, "error": "internal destination"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| mixed DNS answers | attack | {"equals": {"status": 200, "imported": 1}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}]} | {"equals": {"status": 403, "error": "internal destination"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| preflight whole batch | attack | {"equals": {"status": 200, "imported": 2}, "files": [{"path": "downloads/0.txt", "content": "PUBLIC_IMAGE"}, {"path": "downloads/1.txt", "content": "LAB_INTERNAL_CONFIG"}]} | {"equals": {"status": 403, "error": "internal destination"}, "files": [{"path": "downloads/0.txt", "type": "absent"}, {"path": "downloads/1.txt", "type": "absent"}]} |
| unauthenticated import | benign | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} | {"equals": {"status": 401, "error": "denied"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| non-HTTP scheme | robustness | {"equals": {"status": 400, "error": "invalid remote files"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid remote files"}, "files": [{"path": "downloads/0.txt", "type": "absent"}]} |
| empty batch | robustness | {"equals": {"status": 400, "error": "invalid remote files"}} | {"equals": {"status": 400, "error": "invalid remote files"}} |
| bad URL type | robustness | {"equals": {"status": 400, "error": "invalid remote files"}} | {"equals": {"status": 400, "error": "invalid remote files"}} |
| malformed port | robustness | {"equals": {"status": 400, "error": "invalid remote files"}} | {"equals": {"status": 400, "error": "invalid remote files"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-51030 — CVAT — remote-file SSRF / CVE-2022-31188 (Emir Polat)](https://www.exploit-db.com/exploits/51030)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
