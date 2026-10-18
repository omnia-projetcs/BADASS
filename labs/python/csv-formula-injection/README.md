# Csv formula injection

Untrusted descriptions are exported as CSV cells without neutralizing formula-leading characters. Inspired by EDB-49805 (Kimai CSV injection). The fixture writes and verifies real CSV bytes; it does not execute a spreadsheet or assert code execution.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-1236 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use the CSV writer for field boundaries and prefix dangerous values with the literal TEXT: marker. This deliberately changes cell contents for human-review exports; original values are preserved after that prefix. Formula starters, their full-width variants, leading whitespace and control prefixes are covered. Tests establish the exported-cell contract only, not universal behavior of every spreadsheet or later transformation.

## Regression

```sh
python3 tools/lab.py test --case python/csv-formula-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain cells | benign | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Meeting\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Meeting\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Meeting\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Meeting\",\"Alice\"\r\n"}]} |
| quote and separator | benign | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Review, \"\"phase 2\"\"\",\"Zoé\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Review, \"\"phase 2\"\"\",\"Zoé\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Review, \"\"phase 2\"\"\",\"Zoé\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Review, \"\"phase 2\"\"\",\"Zoé\"\r\n"}]} |
| multiple rows | benign | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"One\",\"Alice\"\r\n\"Two\",\"Bob\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"One\",\"Alice\"\r\n\"Two\",\"Bob\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"One\",\"Alice\"\r\n\"Two\",\"Bob\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"One\",\"Alice\"\r\n\"Two\",\"Bob\"\r\n"}]} |
| embedded newline | benign | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"First\nSecond\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"First\nSecond\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"First\nSecond\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"First\nSecond\",\"Alice\"\r\n"}]} |
| empty cells | benign | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"\",\"\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"\",\"\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"\",\"\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"\",\"\"\r\n"}]} |
| equals | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"=1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: =1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: =1+1\",\"Alice\"\r\n"}]} |
| plus | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"+1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"+1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: +1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: +1+1\",\"Alice\"\r\n"}]} |
| minus | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"-1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"-1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: -1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: -1+1\",\"Alice\"\r\n"}]} |
| at | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"@SUM(1,2)\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"@SUM(1,2)\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: @SUM(1,2)\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: @SUM(1,2)\",\"Alice\"\r\n"}]} |
| leading spaces | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"  =1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"  =1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT:   =1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT:   =1+1\",\"Alice\"\r\n"}]} |
| leading tab | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"\t=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"\t=1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: \t=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: \t=1+1\",\"Alice\"\r\n"}]} |
| leading carriage return | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"\r=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"\r=1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: \r=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: \r=1+1\",\"Alice\"\r\n"}]} |
| leading newline | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"\n=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"\n=1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: \n=1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: \n=1+1\",\"Alice\"\r\n"}]} |
| full-width equals | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"＝1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"＝1+1\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: ＝1+1\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: ＝1+1\",\"Alice\"\r\n"}]} |
| full-width at | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"＠SUM(1,2)\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"＠SUM(1,2)\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: ＠SUM(1,2)\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: ＠SUM(1,2)\",\"Alice\"\r\n"}]} |
| quoted separator | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"=1+1\"\";=2+2\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"=1+1\"\";=2+2\",\"Alice\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"TEXT: =1+1\"\";=2+2\",\"Alice\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"TEXT: =1+1\"\";=2+2\",\"Alice\"\r\n"}]} |
| second column is also untrusted | attack | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Meeting\",\"=1+1\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Meeting\",\"=1+1\"\r\n"}]} | {"equals": {"status": 200, "csv": "\"description\",\"owner\"\r\n\"Meeting\",\"TEXT: =1+1\"\r\n"}, "files": [{"path": "export.csv", "content": "\"description\",\"owner\"\r\n\"Meeting\",\"TEXT: =1+1\"\r\n"}]} |
| empty batch | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |
| non-list input | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |
| wrong column count | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |
| non-string cell | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |
| NUL cell | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |
| oversized cell | robustness | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid rows"}, "files": [{"path": "export.csv", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-49805 — Kimai 1.14 CSV Injection — Mohammed Aloraimi](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/49805.txt)
- [OWASP — CSV Injection and spreadsheet-specific limitations](https://owasp.org/www-community/attacks/CSV_Injection)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
