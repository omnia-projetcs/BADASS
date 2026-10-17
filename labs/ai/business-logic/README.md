# Invalid purchase quantity

A negative purchase quantity increases the account balance.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-1284 |
| OWASP | A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce positive bounded purchase quantities before changing the balance.

## Regression

```sh
python3 tools/lab.py test --case ai/business-logic --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary order | benign | {"equals": "980"} | {"equals": "980"} |
| boundary order | benign | {"equals": "0"} | {"equals": "0"} |
| negative order | attack | {"equals": "1050"} | {"equals": "DENIED"} |
| zero order | attack | {"equals": "1000"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
