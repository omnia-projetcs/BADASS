# ActiveMQ: unchecked throwable construction

Original reduced Python model inspired by CVE-2023-46604. A serialized throwable names a class selected from an offline registry. The vulnerable decoder constructs it before checking its exception type; a synthetic context-loader constructor parses XML and writes a real marker file. This models constructor side effects, not Java class loading, OpenWire bytes or broker RCE.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-470 |
| CVE | CVE-2023-46604 |
| OWASP | A05:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the selected class against the permitted exception type before invoking any constructor. The registry is fixed laboratory code with no dynamic imports, and the XML context comes from an offline map. An error response after construction is too late to undo side effects. Actual ActiveMQ/OpenWire remediation requires the upstream fix in clients and brokers.

## Regression

```sh
python3 tools/lab.py test --case python/activemq-openwire-type --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal exception | benign | {"equals": {"status": 200, "error_type": "BrokerError", "message": "queue missing"}} | {"equals": {"status": 200, "error_type": "BrokerError", "message": "queue missing"}} |
| empty exception message | benign | {"equals": {"status": 200, "error_type": "BrokerError", "message": ""}} | {"equals": {"status": 200, "error_type": "BrokerError", "message": ""}} |
| constructor before type validation | attack | {"equals": {"status": 400, "error": "invalid throwable"}, "files": [{"path": "loaded-context.txt", "content": "LAB_CONTEXT_LOADED"}]} | {"equals": {"status": 400, "error": "invalid throwable"}, "files": [{"path": "loaded-context.txt", "type": "absent"}]} |
| extra class metadata cannot authorize construction | attack | {"equals": {"status": 400, "error": "invalid throwable"}, "files": [{"path": "loaded-context.txt", "content": "LAB_CONTEXT_LOADED"}]} | {"equals": {"status": 400, "error": "invalid throwable"}, "files": [{"path": "loaded-context.txt", "type": "absent"}]} |
| unknown class | robustness | {"equals": {"status": 400, "error": "invalid throwable"}} | {"equals": {"status": 400, "error": "invalid throwable"}} |
| class name object | robustness | {"equals": {"status": 400, "error": "invalid throwable"}} | {"equals": {"status": 400, "error": "invalid throwable"}} |
| wrong message type | robustness | {"equals": {"status": 400, "error": "invalid throwable"}} | {"equals": {"status": 400, "error": "invalid throwable"}} |
| oversized message | robustness | {"equals": {"status": 400, "error": "invalid throwable"}} | {"equals": {"status": 400, "error": "invalid throwable"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Apache ActiveMQ CVE-2023-46604 — upstream impact and constructor behavior](https://activemq.apache.org/news/cve-2023-46604)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
