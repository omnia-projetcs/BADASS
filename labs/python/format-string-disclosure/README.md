# Format string disclosure

A caller-controlled Python str.format template receives a rich profile object. Attribute and dictionary traversal in a replacement field exposes a synthetic private API key. This is real Python format-string evaluation, not Jinja/Twig or arbitrary code execution.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-134 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Define a small renderer contract: permit only the public name and team placeholders, reject attribute/item traversal, conversions and format specifications, then format using only those public strings. Preserve literal braces and ordinary text. The fixture tests confidentiality and formatting behavior; it does not model HTML output or a full template engine.

## Regression

```sh
python3 tools/lab.py test --case python/format-string-disclosure --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| public placeholders | benign | {"equals": {"status": 200, "text": "Hello Alice, Engineering"}} | {"equals": {"status": 200, "text": "Hello Alice, Engineering"}} |
| literal text | benign | {"equals": {"status": 200, "text": "Welcome"}} | {"equals": {"status": 200, "text": "Welcome"}} |
| escaped braces | benign | {"equals": {"status": 200, "text": "{name} Alice"}} | {"equals": {"status": 200, "text": "{name} Alice"}} |
| Unicode text | benign | {"equals": {"status": 200, "text": "Équipe : Engineering"}} | {"equals": {"status": 200, "text": "Équipe : Engineering"}} |
| empty template | benign | {"equals": {"status": 200, "text": ""}} | {"equals": {"status": 200, "text": ""}} |
| private attribute and item | attack | {"equals": {"status": 200, "text": "LAB_FORMAT_PRIVATE_KEY"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| dictionary traversal | attack | {"equals": {"status": 200, "text": "LAB_FORMAT_PRIVATE_KEY"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| private dictionary representation | attack | {"equals": {"status": 200, "text": "{'api_key': 'LAB_FORMAT_PRIVATE_KEY'}"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| conversion outside supported contract | functional | {"equals": {"status": 200, "text": "'Alice'"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| format specification outside contract | functional | {"equals": {"status": 200, "text": "   Alice"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| unknown field | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| unclosed field | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| non-string template | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| oversized template | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Python — Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax)
- [MITRE CWE-134 — Use of Externally-Controlled Format String](https://cwe.mitre.org/data/definitions/134.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
