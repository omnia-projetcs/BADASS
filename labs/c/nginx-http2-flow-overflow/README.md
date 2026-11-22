# NGINX2Root: HTTP/2 flow-control window overflow

An original native C model of NGINX2Root HTTP/2 flow-control window overflow. Adding an unchecked 32-bit WINDOW_UPDATE increment wraps the window size to a small allocation while still copying a larger frame payload into the heap staging buffer. AddressSanitizer detects the heap-buffer-overflow. No NGINX code or network listener is embedded.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-190, CWE-787 |
| CVE | CVE-2026-123007 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Reject WINDOW_UPDATE increments that are zero or would exceed the HTTP/2 0x7fffffff window limit using overflow-safe arithmetic, and check frame payload length against the allocated staging buffer before copying. Real NGINX deployments require upgrading to NGINX 1.31.9+ or 1.30.7+.

## Regression

```sh
python3 tools/lab.py test --case c/nginx-http2-flow-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal window update and frame | benign | {"equals": "OK:11"} | {"equals": "OK:11"} |
| zero window increment rejected | benign | {"equals": "FLOW_CONTROL_ERROR"} | {"equals": "FLOW_CONTROL_ERROR"} |
| wrapping window increment causes heap overflow | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "FLOW_CONTROL_ERROR"} |
| window increment exceeding RFC limit | attack | {"equals": "OK:5"} | {"equals": "FLOW_CONTROL_ERROR"} |
| missing separator | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| empty input | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [NGINX CVE-2026-123007 — HTTP/2 flow-control window overflow](https://nginx.org/en/security_advisories.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
