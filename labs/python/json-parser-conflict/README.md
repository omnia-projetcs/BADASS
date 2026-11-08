# Json parser conflict

A gateway validates the first occurrence of each JSON key, but its worker reparses the original text with last-key-wins semantics. A duplicate amount bypasses the per-payment cap and causes a larger committed SQLite debit.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-436 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject duplicate decoded keys, including Unicode-escaped equivalents, and pass the already validated object to the worker. Validate exact schema and integer limits before committing wallet and ledger changes together. This models JSON parser disagreement, not HTTP request smuggling or a network payment service.

## Regression

```sh
python3 tools/lab.py test --case python/json-parser-conflict --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| minimum amount | benign | {"equals": {"status": 201, "amount": 1}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4999, \"payments\": [[1, \"vendor\"]]}\n"}]} | {"equals": {"status": 201, "amount": 1}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4999, \"payments\": [[1, \"vendor\"]]}\n"}]} |
| maximum allowed amount | benign | {"equals": {"status": 201, "amount": 100}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4900, \"payments\": [[100, \"vendor\"]]}\n"}]} | {"equals": {"status": 201, "amount": 100}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4900, \"payments\": [[100, \"vendor\"]]}\n"}]} |
| field order and whitespace | benign | {"equals": {"status": 201, "amount": 39}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4961, \"payments\": [[39, \"vendor\"]]}\n"}]} | {"equals": {"status": 201, "amount": 39}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4961, \"payments\": [[39, \"vendor\"]]}\n"}]} |
| last duplicate changes debit | attack | {"equals": {"status": 201, "amount": 1000}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4000, \"payments\": [[1000, \"vendor\"]]}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| escaped duplicate key | attack | {"equals": {"status": 201, "amount": 713}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4287, \"payments\": [[713, \"vendor\"]]}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| three conflicting values | attack | {"equals": {"status": 201, "amount": 900}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4100, \"payments\": [[900, \"vendor\"]]}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| identical duplicates still ambiguous | functional | {"equals": {"status": 201, "amount": 10}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 4990, \"payments\": [[10, \"vendor\"]]}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| unambiguous excessive amount | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| boolean amount | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| fractional amount | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| negative amount | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| nonfinite amount | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| invalid recipient | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| malformed JSON | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| array root | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| non-string input | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |
| oversized input | robustness | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} | {"equals": {"status": 400}, "files": [{"path": "payments-state.json", "content": "{\"balance\": 5000, \"payments\": []}\n"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-436 — Interpretation Conflict](https://cwe.mitre.org/data/definitions/436.html)
- [Python JSON — Repeated Names Within an Object](https://docs.python.org/3/library/json.html#repeated-names-within-an-object)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
