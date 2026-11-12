# Currency arbitrage

A wallet top-up handler credits the USD balance with the raw numeric amount of a payment settled in a lower-value currency.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-841, CWE-682 |
| OWASP | API6:2023, A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require the payment currency to match the wallet settlement currency and reject unapproved or mismatched currencies before crediting.

## Regression

```sh
python3 tools/lab.py test --case rest-api/currency-arbitrage --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| USD top-up | benign | {"equals": {"wallet_usd": 150, "charged_currency": "USD"}} | {"equals": {"wallet_usd": 150, "charged_currency": "USD"}} |
| JPY currency arbitrage | attack | {"equals": {"wallet_usd": 600, "charged_currency": "JPY"}} | {"equals": "DENIED"} |
| negative top-up | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
