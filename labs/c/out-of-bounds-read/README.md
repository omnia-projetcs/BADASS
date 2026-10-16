# Out of bounds read

An unchecked index reads beyond a stack array.

**Technology:** C  
**CWE:** CWE-125  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Validate both lower and upper index bounds before access.

## Regression

```sh
python3 tools/lab.py test --case c/out-of-bounds-read --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid index | benign | {"equals": "20"} | {"equals": "20"} |
| out of bounds | attack | {"stderr_contains": "AddressSanitizer"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
