# Monetary rounding

Biased floating-point rounding in split payouts credits more cents than were debited from the source account.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-1339, CWE-682 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Compute monetary splits in exact integer cents using quotient and remainder distribution and verify conservation of funds.

## Regression

```sh
python3 tools/lab.py test --case python/monetary-rounding --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| even split | benign | {"equals": {"debited": 100, "credited": 100, "payouts": [50, 50]}} | {"equals": {"debited": 100, "credited": 100, "payouts": [50, 50]}} |
| salami rounding split | attack | {"equals": {"debited": 100, "credited": 102, "payouts": [34, 34, 34]}} | {"equals": {"debited": 100, "credited": 100, "payouts": [34, 33, 33]}} |
| zero splits | robustness | {"stderr_contains": "ZeroDivisionError"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
