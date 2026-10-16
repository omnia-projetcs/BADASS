# Use after free

An object remains accessible after its storage is released.

**Technology:** C++  
**CWE:** CWE-416  
**OWASP:** A06:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.cpp) · [Corrected source](fixed/main.cpp)

## Correction

Clear the released pointer and deny access after its lifetime ends.

## Regression

```sh
python3 tools/lab.py test --case cpp/use-after-free --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid lifetime or length | benign | {"equals": "42"} | {"equals": "42"} |
| invalid lifetime or length | attack | {"stderr_contains": "heap-use-after-free"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
