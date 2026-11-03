# SVG resource SSRF

An authenticated SVG upload follows href and xlink:href resources during server-side processing. A real XML parser feeds an offline endpoint registry and can retrieve synthetic internal content. Inspired by EDB-52551; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-918 |
| OWASP | A01:2025, API7:2023 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Preflight the entire SVG and permit only local fragment references; reject external resources before any fetch. The strict policy also rejects external public images. Authentication is a synthetic tenant-admin token. This bounded handler model parses SVG references but does not render images, execute scripts, perform network requests or reproduce ThingsBoard.

## Regression

```sh
python3 tools/lab.py test --case python/svg-resource-ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty drawing | benign | {"equals": {"status": 200, "resources": []}} | {"equals": {"status": 200, "resources": []}} |
| fragment reference | benign | {"equals": {"status": 200, "resources": []}} | {"equals": {"status": 200, "resources": []}} |
| xlink fragment | benign | {"equals": {"status": 200, "resources": []}} | {"equals": {"status": 200, "resources": []}} |
| loopback image | attack | {"equals": {"status": 200, "resources": ["LAB_INTERNAL_CONFIG"]}} | {"equals": {"status": 403, "error": "external SVG resource"}} |
| xlink metadata | attack | {"equals": {"status": 200, "resources": ["LAB_METADATA"]}} | {"equals": {"status": 403, "error": "external SVG resource"}} |
| public external image disabled | functional | {"equals": {"status": 200, "resources": ["PUBLIC_IMAGE"]}} | {"equals": {"status": 403, "error": "external SVG resource"}} |
| missing authorization | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| malformed XML | robustness | {"equals": {"status": 400, "error": "invalid SVG"}} | {"equals": {"status": 400, "error": "invalid SVG"}} |
| DTD forbidden | robustness | {"equals": {"status": 400, "error": "invalid SVG"}} | {"equals": {"status": 400, "error": "invalid SVG"}} |
| non-string document | robustness | {"equals": {"status": 400, "error": "invalid SVG"}} | {"equals": {"status": 400, "error": "invalid SVG"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-52551 — ThingsBoard 4.2.0 — SVG resource SSRF / CVE-2025-34282 (9tamilmathi)](https://www.exploit-db.com/exploits/52551)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
