# Argument injection

A wrapper passes user input as one argv element to a real child process without a shell, but the child still interprets a leading option. An internal --include-private switch exposes a synthetic private record. Inspired by EDB-44993; the argparse search tool is original laboratory code, not GitList.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-88 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Insert the child tool's -- option terminator before the untrusted positional query. Retain argv execution and the absolute interpreter/source paths. This correction relies on the child parser honoring --; other programs need their own argument contract. Tests use a real bounded subprocess and an internal search option, with no external program, shell command execution or network access.

## Regression

```sh
python3 tools/lab.py test --case python/argument-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public report | benign | {"equals": {"status": 200, "matches": ["PUBLIC_REPORT"]}} | {"equals": {"status": 200, "matches": ["PUBLIC_REPORT"]}} |
| case insensitive search | benign | {"equals": {"status": 200, "matches": ["PUBLIC_NOTES"]}} | {"equals": {"status": 200, "matches": ["PUBLIC_NOTES"]}} |
| empty query | benign | {"equals": {"status": 200, "matches": ["PUBLIC_REPORT", "PUBLIC_NOTES"]}} | {"equals": {"status": 200, "matches": ["PUBLIC_REPORT", "PUBLIC_NOTES"]}} |
| unknown text | benign | {"equals": {"status": 200, "matches": []}} | {"equals": {"status": 200, "matches": []}} |
| shell characters are literal | benign | {"equals": {"status": 200, "matches": []}} | {"equals": {"status": 200, "matches": []}} |
| spaces stay one argument | benign | {"equals": {"status": 200, "matches": []}} | {"equals": {"status": 200, "matches": []}} |
| private option injected | attack | {"equals": {"status": 200, "matches": ["PUBLIC_REPORT", "PUBLIC_NOTES", "LAB_PRIVATE_REPORT"]}} | {"equals": {"status": 200, "matches": []}} |
| help option becomes literal | functional | {"equals": {"status": 400, "error": "invalid tool argument"}} | {"equals": {"status": 200, "matches": []}} |
| unknown option becomes literal | functional | {"equals": {"status": 400, "error": "invalid tool argument"}} | {"equals": {"status": 200, "matches": []}} |
| non-string input | robustness | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 400, "error": "invalid query"}} |
| NUL input | robustness | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 400, "error": "invalid query"}} |
| oversized query | robustness | {"equals": {"status": 400, "error": "invalid query"}} | {"equals": {"status": 400, "error": "invalid query"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-44993 — GitList 0.6.0 Argument Injection — Kacper Szurek / Shelby Pace](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/remote/44993.rb)
- [MITRE CWE-88 — Argument Injection](https://cwe.mitre.org/data/definitions/88.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
