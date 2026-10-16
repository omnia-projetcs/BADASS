# Unverified security claim

A generated claim closes a security finding without independent evidence.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-345  
**OWASP:** LLM09:2025  
**Test scope:** `ai-boundary-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require a trusted regression result before accepting a claimed remediation.

## Regression

```sh
python3 tools/lab.py test --case ai/unverified-security-claim --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| unresolved claim | benign | {"equals": "OPEN"} | {"equals": "OPEN"} |
| unsupported resolution | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
