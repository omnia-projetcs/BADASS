# Signed action replay

A processor verifies a full HMAC and expiry but accepts the same signed action repeatedly. Capturing and replaying identical authenticated bytes causes repeated debits, recorded in an actual ledger snapshot.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-294 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Track successfully consumed signed identifiers and reject reuse before a second debit. Authenticate and validate first; failed or unaffordable actions must not burn their identifiers. The correction is scoped to one sequential processor instance. Production restart and multi-worker guarantees require a durable unique constraint and an atomic transaction; those are not implemented by this local model.

## Regression

```sh
python3 tools/lab.py test --case python/signed-action-replay --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| single signed action | benign | {"equals": {"statuses": [200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} | {"equals": {"statuses": [200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| distinct action identifiers | benign | {"equals": {"statuses": [200, 200], "balance": 750}, "files": [{"path": "ledger.json", "content": "{\"balance\":750,\"accepted\":[{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-2\",\"amount\":150}]}\n"}]} | {"equals": {"statuses": [200, 200], "balance": 750}, "files": [{"path": "ledger.json", "content": "{\"balance\":750,\"accepted\":[{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-2\",\"amount\":150}]}\n"}]} |
| last valid instant | benign | {"equals": {"statuses": [200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} | {"equals": {"statuses": [200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| forged then genuine proof | benign | {"equals": {"statuses": [401, 200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} | {"equals": {"statuses": [401, 200], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| expired proof | benign | {"equals": {"statuses": [401], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} | {"equals": {"statuses": [401], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} |
| exact expiry boundary | benign | {"equals": {"statuses": [401], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} | {"equals": {"statuses": [401], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} |
| insufficient balance | benign | {"equals": {"statuses": [200, 200, 402], "balance": 0}, "files": [{"path": "ledger.json", "content": "{\"balance\":0,\"accepted\":[{\"id\":\"event-1\",\"amount\":500},{\"id\":\"event-2\",\"amount\":500}]}\n"}]} | {"equals": {"statuses": [200, 200, 402], "balance": 0}, "files": [{"path": "ledger.json", "content": "{\"balance\":0,\"accepted\":[{\"id\":\"event-1\",\"amount\":500},{\"id\":\"event-2\",\"amount\":500}]}\n"}]} |
| identical proof twice | attack | {"equals": {"statuses": [200, 200], "balance": 800}, "files": [{"path": "ledger.json", "content": "{\"balance\":800,\"accepted\":[{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-1\",\"amount\":100}]}\n"}]} | {"equals": {"statuses": [200, 409], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| three deliveries of one action | attack | {"equals": {"statuses": [200, 200, 200], "balance": 700}, "files": [{"path": "ledger.json", "content": "{\"balance\":700,\"accepted\":[{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-1\",\"amount\":100}]}\n"}]} | {"equals": {"statuses": [200, 409, 409], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| reused signed identifier with changed amount | attack | {"equals": {"statuses": [200, 200], "balance": 750}, "files": [{"path": "ledger.json", "content": "{\"balance\":750,\"accepted\":[{\"id\":\"event-1\",\"amount\":100},{\"id\":\"event-1\",\"amount\":150}]}\n"}]} | {"equals": {"statuses": [200, 409], "balance": 900}, "files": [{"path": "ledger.json", "content": "{\"balance\":900,\"accepted\":[{\"id\":\"event-1\",\"amount\":100}]}\n"}]} |
| invalid signed identifier | robustness | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} |
| boolean signed amount | robustness | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} |
| missing signed amount | robustness | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} | {"equals": {"statuses": [400], "balance": 1000}, "files": [{"path": "ledger.json", "content": "{\"balance\":1000,\"accepted\":[]}\n"}]} |
| empty actions | robustness | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} |
| non-object request | robustness | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} |
| unknown signature mode | robustness | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} |
| backwards clock | robustness | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "ledger.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-294](https://cwe.mitre.org/data/definitions/294.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
