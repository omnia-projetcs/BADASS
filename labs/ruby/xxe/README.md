# XML external entities (XXE)

Resolving SYSTEM entities in an untrusted XML document reads local files such as secret.txt into the parsed response.

| Attribute | Value |
|---|---|
| Technology | Ruby |
| CWE | CWE-611 |
| OWASP | A02:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.rb) · [Corrected source](fixed/main.rb)

## Correction

Forbid DOCTYPE and ENTITY declarations and disable external entity resolution in the XML parser.

## Regression

```sh
python3 tools/lab.py test --case ruby/xxe --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain XML element | benign | {"equals": "hello"} | {"equals": "hello"} |
| external file entity | attack | {"equals": "LAB_SECRET"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
