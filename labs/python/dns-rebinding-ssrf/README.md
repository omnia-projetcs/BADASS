# DNS rebinding SSRF

An outbound handler validates a DNS answer, then resolves again at connection time. A deterministic resolver changes from a public address to an internal address and a synthetic transport exposes an internal service marker. Inspired by EDB-52651; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-918 |
| OWASP | A01:2025, API7:2023 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate all returned addresses and pass the chosen validated address directly to the transport, preserving the original host separately. The resolver sequences and transport are trusted fixture dependencies, not request parameters. This is a handler model: no DNS, socket, TLS or HTTP request occurs; production code also needs redirect, proxy and TLS policy.

## Regression

```sh
python3 tools/lab.py test --case python/dns-rebinding-ssrf --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| stable public DNS | benign | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} |
| public literal address | benign | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} |
| private first answer denied | benign | {"equals": {"status": 403, "error": "internal destination"}} | {"equals": {"status": 403, "error": "internal destination"}} |
| rebind to loopback | attack | {"equals": {"status": 200, "body": "LAB_INTERNAL_SERVICE"}} | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} |
| rebind to link-local | attack | {"equals": {"status": 200, "body": "LAB_INTERNAL_SERVICE"}} | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} |
| mixed answer set | attack | {"equals": {"status": 200, "body": "PUBLIC_IMAGE"}} | {"equals": {"status": 403, "error": "internal destination"}} |
| credentials forbidden | robustness | {"equals": {"status": 400, "error": "invalid URL"}} | {"equals": {"status": 400, "error": "invalid URL"}} |
| invalid port | robustness | {"equals": {"status": 400, "error": "invalid URL"}} | {"equals": {"status": 400, "error": "invalid URL"}} |
| unknown host | robustness | {"equals": {"status": 400, "error": "invalid URL"}} | {"equals": {"status": 400, "error": "invalid URL"}} |
| wrong type | robustness | {"equals": {"status": 400, "error": "invalid URL"}} | {"equals": {"status": 400, "error": "invalid URL"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-52651 — flyto_core 2.26.7 — DNS rebinding SSRF (Jorge González Milla)](https://www.exploit-db.com/exploits/52651)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
