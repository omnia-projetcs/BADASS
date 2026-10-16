# Integer overflow

Wrapping arithmetic undercharges an order.

**Technology:** Rust  
**CWE:** CWE-190  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.rs) · [Corrected source](fixed/main.rs)

## Correction

Use checked arithmetic and reject out-of-range totals.

## Regression

```sh
python3 tools/lab.py test --case rust/integer-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| one item | benign | {"equals": "100"} | {"equals": "100"} |
| overflow | attack | {"equals": "4"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
