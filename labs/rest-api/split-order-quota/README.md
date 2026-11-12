# Split order quota

Splitting an order into multiple smaller line items bypasses the per-request quantity cap and exceeds the account quota.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-799, CWE-841 |
| OWASP | API6:2023, A06:2025 |
| Test scope | `state-machine-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate cumulative account usage against the quota inside the database transaction before committing new orders.

## Regression

```sh
python3 tools/lab.py test --case rest-api/split-order-quota --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| within quota split | benign | {"equals": {"status": 200, "allocated": 90}} | {"equals": {"status": 200, "allocated": 90}} |
| quota bypass via split orders | attack | {"equals": {"status": 200, "allocated": 120}} | {"equals": "DENIED"} |
| empty order list | robustness | {"equals": {"status": 200, "allocated": 0}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
