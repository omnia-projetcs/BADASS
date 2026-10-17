# Broken authentication

Any nonempty bearer value is accepted as authentication.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-287 |
| OWASP | API2:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate the request schema and full ASCII bearer value against the synthetic server-side credential. Invalid types and non-ASCII values return 401 without an exception.

## Regression

```sh
python3 tools/lab.py test --case rest-api/broken-authentication --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid token | benign | {"equals": {"status": 200}} | {"equals": {"status": 200}} |
| forged token | attack | {"equals": {"status": 200}} | {"equals": {"status": 401}} |
| missing token | benign | {"equals": {"status": 401}} | {"equals": {"status": 401}} |
| non-ASCII bearer value | robustness | {"equals": {"status": 200}} | {"equals": {"status": 401}} |
| null bearer value | robustness | {"equals": {"status": 401}} | {"equals": {"status": 401}} |
| structured bearer value | robustness | {"equals": {"status": 200}} | {"equals": {"status": 401}} |
| non-object request | robustness | {"stderr_contains": "AttributeError"} | {"equals": {"status": 401}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
