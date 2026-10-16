# Integer overflow

Unsigned multiplication wraps and undercharges an order.

**Technology:** C  
**CWE:** CWE-190  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Check the multiplication bound before computing the total.

## Regression

```sh
python3 tools/lab.py test --case c/integer-overflow --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal order | benign | {"equals": "100"} | {"equals": "100"} |
| largest safe quantity | benign | {"equals": "4294967200"} | {"equals": "4294967200"} |
| wrapping order | attack | {"equals": "4"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
