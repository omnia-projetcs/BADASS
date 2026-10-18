# XML external entities (XXE)

A SAX parser expands attacker-declared external entities and includes local file contents in parsed text. Inspired by EDB-43113, the Ladon advisory. This original Python parser fixture reads only synthetic files in regression tests; it is not a Ladon service.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-611 |
| OWASP | A02:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Disable external general entities and reject every DTD via the parser lexical handler before entity resolution. Preserve ordinary XML text, built-in entities and CDATA. A local-file-only resolver bounds the vulnerable demonstration; HTTP entities, SOAP dispatch and resource-exhaustion attacks are outside this fixture.

## Regression

```sh
python3 tools/lab.py test --case python/xxe --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain text | benign | {"equals": {"status": 200, "text": "Hello"}} | {"equals": {"status": 200, "text": "Hello"}} |
| built-in entities | benign | {"equals": {"status": 200, "text": "A &amp; B &lt; C"}} | {"equals": {"status": 200, "text": "A &amp; B &lt; C"}} |
| CDATA | benign | {"equals": {"status": 200, "text": "&lt;!DOCTYPE is literal text&gt;"}} | {"equals": {"status": 200, "text": "&lt;!DOCTYPE is literal text&gt;"}} |
| nested Unicode | benign | {"equals": {"status": 200, "text": "Salut Zoé !"}} | {"equals": {"status": 200, "text": "Salut Zoé !"}} |
| XML comment | benign | {"equals": {"status": 200, "text": "Hello"}} | {"equals": {"status": 200, "text": "Hello"}} |
| local secret | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| second local file | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| encoded local filename | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| internal DTD disallowed | functional | {"equals": {"status": 200, "text": "Hello"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| non-string input | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| empty XML | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| malformed XML | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| undefined entity | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| oversized XML | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| missing local file | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |
| network entity blocked | robustness | {"equals": {"status": 400, "error": "invalid XML"}} | {"equals": {"status": 400, "error": "invalid XML"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-43113 — Ladon Framework for Python 0.9.40 XML External Entity Expansion — RedTeam Pentesting](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/xml/webapps/43113.txt)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
