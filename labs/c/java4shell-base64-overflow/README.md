# Java4Shell: vectorized Base64 padding overflow

An original native C model of Java4Shell (OpenJDK HotSpot AVX-512 Base64 heap overflow). When decoding inputs that take the vectorized fast path, unconditionally writing full 3-byte output groups despite trailing '=' padding writes past the exact-sized heap buffer. AddressSanitizer observes an actual heap-buffer-overflow. No JVM or AVX-512 assembly is embedded.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-787 |
| CVE | CVE-2026-114938 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Validate Base64 padding placement before decoding, emit only the decoded bytes not suppressed by trailing '=' characters, and enforce output-buffer capacity checks before every store. Real Java deployments require updating OpenJDK/Oracle JDK 17, 21, 25 or 27 to patched releases.

## Regression

```sh
python3 tools/lab.py test --case c/java4shell-base64-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| short unpadded base64 | benign | {"equals": "OK:3"} | {"equals": "OK:3"} |
| short padded base64 scalar path | benign | {"equals": "OK:5"} | {"equals": "OK:5"} |
| fast-path unpadded base64 | benign | {"equals": "OK:15"} | {"equals": "OK:15"} |
| fast-path trailing double padding overflow | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "OK:16"} |
| fast-path trailing single padding overflow | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "OK:17"} |
| non-multiple-of-4 input | robustness | {"equals": "FORMAT_ERROR"} | {"equals": "FORMAT_ERROR"} |
| empty input | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [OpenJDK / Oracle Java CVE-2026-114938 — Java4Shell Base64 heap overflow](https://www.cve.org/CVERecord?id=CVE-2026-114938)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
