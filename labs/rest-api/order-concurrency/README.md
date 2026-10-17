# Concurrent duplicate shipment

Two real local worker threads observe a paid order before writing and both create a shipment from a stale state check.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-362 |
| OWASP | A06:2025, API6:2023 |
| Test scope | `transaction-concurrency-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Acquire a SQLite write transaction, conditionally transition the paid order, and insert a shipment only when the transition changes one row. This fixture covers local transactions, not distributed or crash-safe external dispatch.

## Regression

```sh
python3 tools/lab.py test --case rest-api/order-concurrency --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| one paid order request delivers once | benign | {"equals": {"status": 200, "requests": 1, "accepted": 1, "rejected": 0, "state": "delivered", "shipments": 1}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\n"}]} | {"equals": {"status": 200, "requests": 1, "accepted": 1, "rejected": 0, "state": "delivered", "shipments": 1}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\n"}]} |
| two concurrent requests cannot both claim delivery | attack | {"equals": {"status": 200, "requests": 2, "accepted": 2, "rejected": 0, "state": "delivered", "shipments": 2}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\nLAB_ORDER_1\n"}]} | {"equals": {"status": 200, "requests": 2, "accepted": 1, "rejected": 1, "state": "delivered", "shipments": 1}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\n"}]} |
| client state does not seed the paid server order | benign | {"equals": {"status": 200, "requests": 1, "accepted": 1, "rejected": 0, "state": "delivered", "shipments": 1}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\n"}]} | {"equals": {"status": 200, "requests": 1, "accepted": 1, "rejected": 0, "state": "delivered", "shipments": 1}, "files": [{"path": "order-concurrency.sqlite", "type": "file"}, {"path": "shipments.log", "type": "file", "content": "LAB_ORDER_1\n"}]} |
| zero requests | robustness | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} |
| too many requests | robustness | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} |
| boolean is not an integer request count | robustness | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} |
| string is not an integer request count | robustness | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} |
| missing request count | robustness | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "requests must be 1 or 2"}, "files": [{"path": "order-concurrency.sqlite", "type": "absent"}, {"path": "shipments.log", "type": "absent"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
