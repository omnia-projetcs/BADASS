# Webhook signature

A webhook computes an HMAC-SHA256 signature but discards the comparison result. A well-formed forged digest or a signature for another body still marks a real SQLite invoice as paid.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-347 |
| OWASP | A04:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require a full matching HMAC over the exact raw body before parsing JSON or mutating invoices. Keep schema and invoice-total validation after authentication. The harness creates fresh synthetic keys and signatures locally; no webhook server or signing endpoint is exposed. Delivery replay protection is outside this signature-verification case.

## Regression

```sh
python3 tools/lab.py test --case python/webhook-signature --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| signed first invoice | benign | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} |
| signed second invoice | benign | {"equals": {"status": 200, "invoice": 2}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 1]]\n"}]} | {"equals": {"status": 200, "invoice": 2}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 1]]\n"}]} |
| signed whitespace | benign | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} |
| forged digest | attack | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| different signed body | attack | {"equals": {"status": 200, "invoice": 2}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 1]]\n"}]} | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| wrong signing key | attack | {"equals": {"status": 200, "invoice": 1}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 1], [2, 250, 0]]\n"}]} | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| missing signature | robustness | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| malformed signature | robustness | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 401}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| malformed JSON | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| duplicate field | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| amount mismatch | robustness | {"equals": {"status": 409}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 409}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| unknown invoice | robustness | {"equals": {"status": 404}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 404}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| boolean amount | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| unexpected field | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices-state.json", "content": "[[1, 120, 0], [2, 250, 0]]\n"}]} |
| non-string body | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices.sqlite", "type": "absent"}, {"path": "invoices-state.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices.sqlite", "type": "absent"}, {"path": "invoices-state.json", "type": "absent"}]} |
| oversized body | robustness | {"equals": {"status": 400}, "files": [{"path": "invoices.sqlite", "type": "absent"}, {"path": "invoices-state.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "invoices.sqlite", "type": "absent"}, {"path": "invoices-state.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-347 — Improper Verification of Cryptographic Signature](https://cwe.mitre.org/data/definitions/347.html)
- [GitHub — Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
