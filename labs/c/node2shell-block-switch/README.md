# Node2Shell: Brotli block-switch status

An original C streaming-decoder model of Node2Shell/Brotli. An impossible block switch is confused with temporary input starvation. Repeated feeds append into a real eight-byte heap buffer until AddressSanitizer detects an out-of-bounds write. The simplified category/type/payload grammar is not a Brotli stream, and the fixture does not reproduce Node.js RCE.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-252, CWE-787 |
| CVE | CVE-2026-111497 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Return a permanent format-error status for an impossible block switch, propagate it through literal, command and distance paths, and retain a staging-buffer capacity check. Short malformed streams must be rejected too, so a bounds check alone is an incomplete repair. The Node.js project rates this issue high; the CVE also has a critical CVSS v4 score. Real remediation is a fixed Node.js/Brotli runtime. See the named-CVE guide for sourced version boundaries.

## Regression

```sh
python3 tools/lab.py test --case c/node2shell-block-switch --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| literal valid stream | benign | {"equals": "OK:11"} | {"equals": "OK:11"} |
| command valid stream | benign | {"equals": "OK:11"} | {"equals": "OK:11"} |
| distance valid stream | benign | {"equals": "OK:11"} | {"equals": "OK:11"} |
| valid stream needs input | benign | {"equals": "NEEDS_MORE_INPUT"} | {"equals": "NEEDS_MORE_INPUT"} |
| literal short malformed switch | attack | {"equals": "NEEDS_MORE_INPUT"} | {"equals": "FORMAT_ERROR"} |
| command short malformed switch | attack | {"equals": "NEEDS_MORE_INPUT"} | {"equals": "FORMAT_ERROR"} |
| distance short malformed switch | attack | {"equals": "NEEDS_MORE_INPUT"} | {"equals": "FORMAT_ERROR"} |
| literal ninth buffered byte | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "FORMAT_ERROR"} |
| command ninth buffered byte | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "FORMAT_ERROR"} |
| distance ninth buffered byte | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "FORMAT_ERROR"} |
| zero block types overflow | attack | {"stderr_contains": "AddressSanitizer: heap-buffer-overflow"} | {"equals": "FORMAT_ERROR"} |
| malformed switch without bytes | attack | {"equals": "NEEDS_MORE_INPUT"} | {"equals": "FORMAT_ERROR"} |
| unknown category | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| bad type count | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| oversized feed | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| missing separators | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Node.js CVE-2026-111497 — October 2026 security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
- [Brotli upstream block-switch correction, commit 0ed4268](https://github.com/google/brotli/commit/0ed4268a4401abcb4472096340477cf4af7d1a2b)
- [Brotli 1.2.1 security release](https://github.com/google/brotli/releases/tag/v1.2.1)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
