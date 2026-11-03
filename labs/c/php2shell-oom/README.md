# PHP2Shell: request OOM cleanup

An original native C model of PHP2Shell request-cleanup corruption. A deterministic allocation failure interrupts replacement of request-owned memory; shutdown then reads freed storage. AddressSanitizer observes an actual use-after-free. This is not PHP itself, a multipart parser or an RCE reproduction.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-416 |
| CVE | CVE-2026-109618 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Stage and initialize replacement allocations without publishing partial state. Handle allocation failure by returning to a safe cleanup point, preserving the old value until the replacement is complete. The failure is injected into tiny allocations, not caused by exhausting host memory. Real PHP requires the upstream runtime fix: its soft/hard OOM strategy is broader than this reduced transactional model.

## Regression

```sh
python3 tools/lab.py test --case c/php2shell-oom --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal replacement | benign | {"equals": "UPDATED"} | {"equals": "UPDATED"} |
| request without replacement | benign | {"equals": "READY"} | {"equals": "READY"} |
| failure while replacing value | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "OOM_SAFE"} |
| failure in later allocation | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "OOM_SAFE"} |
| unknown operation | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| empty operation | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2026-109618 — RCE via OOM corruption](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w)
- [PHP security release — 21 October 2026](https://www.php.net/archive/2026.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
