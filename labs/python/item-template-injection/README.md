# Item-name template injection

An item name is concatenated into a text template before compilation. A bounded, original arithmetic template engine evaluates embedded expressions instead of displaying the name as data. Inspired by EDB-52030; this is an original laboratory model of the specified boundary, not a reproduction of the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-1336 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Compile only the trusted template and substitute the name as a value. The teaching engine implements integer addition, subtraction and multiplication via AST, with size and node limits; it has no Python eval, attribute access, filesystem access or code execution. The EDB report demonstrates expression evaluation; this fixture makes no claim about further impact or the vendor engine.

## Regression

```sh
python3 tools/lab.py test --case python/item-template-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal name | benign | {"equals": {"status": 200, "text": "Item: Notebook"}} | {"equals": {"status": 200, "text": "Item: Notebook"}} |
| unicode name | benign | {"equals": {"status": 200, "text": "Item: Café"}} | {"equals": {"status": 200, "text": "Item: Café"}} |
| empty name | benign | {"equals": {"status": 200, "text": "Item: "}} | {"equals": {"status": 200, "text": "Item: "}} |
| arithmetic in name | attack | {"equals": {"status": 200, "text": "Item: 49"}} | {"equals": {"status": 200, "text": "Item: {{7*7}}"}} |
| second expression | attack | {"equals": {"status": 200, "text": "Item: Lot 12"}} | {"equals": {"status": 200, "text": "Item: Lot {{10+2}}"}} |
| unknown expression stays data | functional | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 200, "text": "Item: {{ customer }}"}} |
| missing name | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| non-string name | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |
| oversized name | robustness | {"equals": {"status": 400, "error": "invalid template"}} | {"equals": {"status": 400, "error": "invalid template"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-52030 — Akaunting 3.1.8 — Server-Side Template Injection (tmrswrr)](https://www.exploit-db.com/exploits/52030)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
