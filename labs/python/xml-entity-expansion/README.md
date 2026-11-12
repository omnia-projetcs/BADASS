# XML entity expansion (Billion Laughs)

Nested internal XML entity declarations expand exponentially (Billion Laughs), amplifying memory consumption from a small input.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-776 |
| OWASP | A02:2025, A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Forbid DOCTYPE and ENTITY declarations in untrusted XML documents and enforce strict input and text-node size bounds.

## Regression

```sh
python3 tools/lab.py test --case python/xml-entity-expansion --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain XML element | benign | {"equals": {"length": 5, "preview": "HELLO"}} | {"equals": {"length": 5, "preview": "HELLO"}} |
| nested entity amplification | attack | {"equals": {"length": 64, "preview": "HAHAHAHAHAHAHAHA"}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
