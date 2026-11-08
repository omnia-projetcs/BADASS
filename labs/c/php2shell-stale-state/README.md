# PHP2Shell: stale worker state

An original C worker-lifetime model of PHP2Shell stale request-owned globals. A fatal producer path or a late shutdown diagnostic leaves a global pointing into a freed request. A second request on the same modeled worker reads it before initialization; AddressSanitizer detects the actual use-after-free. No PHP runtime or exploit chain is embedded.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-416 |
| CVE | CVE-2026-109619 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Clear worker references after all shutdown callbacks and before freeing their request-owned storage, including interrupted and late-diagnostic paths. Test both a pre-initialization warning and upload-progress-like consumer, plus controls with no consumer or a new worker. This models ownership and reset ordering only; actual PHP remediation is updating its runtime, not inserting userland session_start or relying on application filtering.

## Regression

```sh
python3 tools/lab.py test --case c/php2shell-stale-state --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal warning consumer | benign | {"equals": "RESET"} | {"equals": "RESET"} |
| normal upload consumer | benign | {"equals": "RESET"} | {"equals": "RESET"} |
| producer without consumer | benign | {"equals": "IDLE"} | {"equals": "IDLE"} |
| new worker control | benign | {"equals": "RESET"} | {"equals": "RESET"} |
| fatal producer then warning | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "RESET"} |
| fatal producer then upload | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "RESET"} |
| late diagnostic then warning | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "RESET"} |
| late diagnostic then upload | attack | {"stderr_contains": "AddressSanitizer: heap-use-after-free"} | {"equals": "RESET"} |
| unknown sequence | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| empty sequence | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2026-109619 — RCE via stale global state](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)
- [PHP security release — 21 October 2026](https://www.php.net/archive/2026.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
