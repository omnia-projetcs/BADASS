# XPath predicate injection

Interpolating user input into an XPath attribute predicate alters the path traversal and exposes privileged XML nodes.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-643 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate account identifiers against a strict allowlist and compare XML element attributes programmatically rather than concatenating XPath predicates.

## Regression

```sh
python3 tools/lab.py test --case python/xpath-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| authorized user node | benign | {"equals": "ALICE_NOTE"} | {"equals": "ALICE_NOTE"} |
| predicate breakout to admin node | attack | {"equals": "LAB_ADMIN_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
