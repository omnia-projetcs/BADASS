# MinIO: bootstrap credential disclosure

Original reduced Python model inspired by CVE-2023-28432. A distributed bootstrap verification handler returns synthetic server configuration without checking its peer token. Its response includes a root credential marker. The configuration is a trusted fixture dependency, not host environment collection; no real MinIO deployment or network service is used.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-306 |
| CVE | CVE-2023-28432 |
| OWASP | A07:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Authenticate the internode token before loading or serializing server configuration. A valid peer must retain access, while arbitrary self-asserted peer headers convey no privilege. Tests replace the configuration dependency with distinct values to verify the disclosure boundary. Actual remediation requires the MinIO fix.

## Regression

```sh
python3 tools/lab.py test --case python/minio-bootstrap-disclosure --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid cluster peer | benign | {"equals": {"status": 200, "environment": {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}}} | {"equals": {"status": 200, "environment": {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}}} |
| unknown route | benign | {"equals": {"status": 404, "error": "missing route"}} | {"equals": {"status": 404, "error": "missing route"}} |
| anonymous configuration disclosure | attack | {"equals": {"status": 200, "environment": {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}}} | {"equals": {"status": 401, "error": "denied"}} |
| invalid token configuration disclosure | attack | {"equals": {"status": 200, "environment": {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}}} | {"equals": {"status": 401, "error": "denied"}} |
| self asserted peer has no identity | attack | {"equals": {"status": 200, "environment": {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}}} | {"equals": {"status": 401, "error": "denied"}} |
| token object | robustness | {"equals": {"status": 400, "error": "invalid peer token"}} | {"equals": {"status": 400, "error": "invalid peer token"}} |
| oversized token | robustness | {"equals": {"status": 400, "error": "invalid peer token"}} | {"equals": {"status": 400, "error": "invalid peer token"}} |
| wrong request shape | robustness | {"equals": {"status": 404, "error": "missing route"}} | {"equals": {"status": 404, "error": "missing route"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MinIO CVE-2023-28432 — information disclosure in cluster deployment](https://github.com/minio/minio/security/advisories/GHSA-6xvq-wj2x-3h3q)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
