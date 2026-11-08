# Invalid purchase quantity

A negative order quantity credits the customer balance.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-1284 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate business invariants before updating the balance.

## Regression

```sh
python3 tools/lab.py test --case python/business-logic --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal purchase | benign | {"equals": 980} | {"equals": 980} |
| negative purchase | attack | {"equals": 1050} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
