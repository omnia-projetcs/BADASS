# Hardcoded credentials

An embedded default password grants administrative access.

**Technology:** Rust  
**CWE:** CWE-798  
**OWASP:** A07:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.rs) · [Corrected source](fixed/main.rs)

## Correction

Remove the embedded credential and require an independently configured secret; fail closed when absent.

## Regression

```sh
python3 tools/lab.py test --case rust/hardcoded-credentials --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| wrong credential | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| empty credential | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| embedded credential | attack | {"equals": "ADMIN"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
