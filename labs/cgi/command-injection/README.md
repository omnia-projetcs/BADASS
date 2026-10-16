# Command injection

A client value is concatenated into a shell command.

**Technology:** CGI (Python)  
**CWE:** CWE-78  
**OWASP:** A05:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Pass the value as one argument to a fixed executable without a shell.

## Regression

```sh
python3 tools/lab.py test --case cgi/command-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary argument | benign | {"equals": "Content-Type: application/json\r\n\r\n\"hello\""} | {"equals": "Content-Type: application/json\r\n\r\n\"hello\""} |
| shell command | attack | {"equals": "Content-Type: application/json\r\n\r\n\"helloBADASS_INJECTED\""} | {"equals": "Content-Type: application/json\r\n\r\n\"hello; printf BADASS_INJECTED\""} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
