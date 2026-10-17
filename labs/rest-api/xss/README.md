# Cross-site scripting (XSS)

Untrusted data is rendered in an HTML body without encoding.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-79 |
| OWASP | A05:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Encode text for the HTML body context.

## Regression

```sh
python3 tools/lab.py test --case rest-api/xss --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary text | benign | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} |
| injected markup | attack | {"equals": "&lt;p&gt;&lt;script&gt;alert(1)&lt;/script&gt;&lt;/p&gt;"} | {"equals": "&lt;p&gt;&amp;lt;script&amp;gt;alert(1)&amp;lt;/script&amp;gt;&lt;/p&gt;"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
