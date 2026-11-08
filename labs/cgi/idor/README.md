# Insecure direct object reference (IDOR)

A caller selects another account without an ownership check.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-639 |
| OWASP | A01:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Compare the selected account owner with the trusted authenticated principal.

## Regression

```sh
python3 tools/lab.py test --case cgi/idor --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| own account | benign | {"equals": "Content-Type: application/json\r\n\r\n\"ALICE_DATA\""} | {"equals": "Content-Type: application/json\r\n\r\n\"ALICE_DATA\""} |
| missing account | benign | {"equals": "Content-Type: application/json\r\n\r\n\"NOT_FOUND\""} | {"equals": "Content-Type: application/json\r\n\r\n\"NOT_FOUND\""} |
| other account | attack | {"equals": "Content-Type: application/json\r\n\r\n\"BOB_PRIVATE\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
