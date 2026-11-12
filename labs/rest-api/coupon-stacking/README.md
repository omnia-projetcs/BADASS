# Coupon stacking

Repeated promotional codes in a single checkout request stack discounts below the minimum price floor.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-841 |
| OWASP | API6:2023, A06:2025 |
| Test scope | `state-machine-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allow at most one validated promotional code per order, reject duplicate or unknown codes, and enforce a minimum payable floor.

## Regression

```sh
python3 tools/lab.py test --case rest-api/coupon-stacking --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| single valid coupon | benign | {"equals": {"status": 200, "total": 70}} | {"equals": {"status": 200, "total": 70}} |
| no coupon checkout | benign | {"equals": {"status": 200, "total": 100}} | {"equals": {"status": 200, "total": 100}} |
| stacked duplicate coupons | attack | {"equals": {"status": 200, "total": -20}} | {"equals": "DENIED"} |
| unknown coupon code | robustness | {"equals": {"status": 200, "total": 100}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
