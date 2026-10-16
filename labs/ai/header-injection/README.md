# HTTP response header injection

An untrusted display name injects another HTTP response header.

**Technology:** AI / LLM boundaries  
**CWE:** CWE-113  
**OWASP:** A05:2025  
**Test scope:** `handler-unit`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject carriage returns and line feeds before constructing header fields.

## Regression

```sh
python3 tools/lab.py test --case ai/header-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary header | benign | {"equals": "X-User: alice\r\n\r\nBODY"} | {"equals": "X-User: alice\r\n\r\nBODY"} |
| CRLF header | attack | {"equals": "X-User: alice\r\nX-Admin: true\r\n\r\nBODY"} | {"equals": "DENIED"} |
| LF header | attack | {"equals": "X-User: alice\nX-Admin: true\r\n\r\nBODY"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
