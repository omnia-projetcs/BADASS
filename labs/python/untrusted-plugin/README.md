# Untrusted plugin

A plugin loader executes a client-supplied source path.

**Technology:** Python  
**CWE:** CWE-829  
**OWASP:** A03:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Select plugins from a trusted registry owned by the application.

## Regression

```sh
python3 tools/lab.py test --case python/untrusted-plugin --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| trusted plugin | benign | {"equals": "OK"} | {"equals": "OK"} |
| untrusted plugin | attack | {"equals": "LAB_EXECUTED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
