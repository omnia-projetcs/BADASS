# Hardcoded credentials

An embedded default password grants administrative access.

| Attribute | Value |
|---|---|
| Technology | CGI (Python) |
| CWE | CWE-798 |
| OWASP | A07:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Remove the embedded credential and require an independently configured secret. Fail closed when absent; validate input types and compare strict UTF-8 bytes so configured Unicode passwords work. Synthetic environment configuration is trusted test metadata.

## Regression

```sh
python3 tools/lab.py test --case cgi/hardcoded-credentials --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| wrong credential | benign | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| empty credential | benign | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| embedded credential | attack | {"equals": "Content-Type: application/json\r\n\r\n\"ADMIN\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| configured credential succeeds | functional | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"ADMIN\""} |
| wrong configured credential | benign | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| configured Unicode credential succeeds | functional | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"ADMIN\""} |
| non-ASCII wrong credential | robustness | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |
| invalid UTF-8 percent encoding | robustness | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"DENIED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
