# Partial HMAC comparison

An HMAC verifier compares only the prefix whose length is chosen by the supplied tag. Empty and truncated tags can authenticate a message, which is then written to a real file. The fixture computes real HMAC-SHA256 values with a fresh synthetic key.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-187 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Require exactly 64 lowercase hexadecimal characters and compare the complete tag with the complete expected HMAC. Constant-time comparison alone does not fix truncation. The signature selectors belong to a local test harness, not a signing API. Delivery replay and transport authentication are outside scope.

## Regression

```sh
python3 tools/lab.py test --case node/partial-signature --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary signed message | benign | {"equals": "{\"status\":201,\"bytes\":13}", "files": [{"path": "verified-message.txt", "content": "PUBLIC_REPORT"}]} | {"equals": "{\"status\":201,\"bytes\":13}", "files": [{"path": "verified-message.txt", "content": "PUBLIC_REPORT"}]} |
| signed Unicode message | benign | {"equals": "{\"status\":201,\"bytes\":9}", "files": [{"path": "verified-message.txt", "content": "Résumé\n"}]} | {"equals": "{\"status\":201,\"bytes\":9}", "files": [{"path": "verified-message.txt", "content": "Résumé\n"}]} |
| signed empty message | benign | {"equals": "{\"status\":201,\"bytes\":0}", "files": [{"path": "verified-message.txt", "content": ""}]} | {"equals": "{\"status\":201,\"bytes\":0}", "files": [{"path": "verified-message.txt", "content": ""}]} |
| maximum body size | benign | {"equals": "{\"status\":201,\"bytes\":256}", "files": [{"path": "verified-message.txt", "content": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}]} | {"equals": "{\"status\":201,\"bytes\":256}", "files": [{"path": "verified-message.txt", "content": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}]} |
| empty tag bypass | attack | {"equals": "{\"status\":201,\"bytes\":14}", "files": [{"path": "verified-message.txt", "content": "FORGED_MESSAGE"}]} | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| short matching tag | attack | {"equals": "{\"status\":201,\"bytes\":14}", "files": [{"path": "verified-message.txt", "content": "FORGED_MESSAGE"}]} | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| empty tag different body | attack | {"equals": "{\"status\":201,\"bytes\":15}", "files": [{"path": "verified-message.txt", "content": "CHANGED_CONTENT"}]} | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| wrong tag | robustness | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| malformed tag | robustness | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":401}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| non-object request | robustness | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| non-string body | robustness | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| oversized UTF-8 body | robustness | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| unknown selector | robustness | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |
| missing selector | robustness | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "verified-message.txt", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-187 — Partial String Comparison](https://cwe.mitre.org/data/definitions/187.html)
- [Node.js crypto timingSafeEqual](https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
