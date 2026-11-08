# Cross-site scripting (XSS)

Untrusted text reaches an HTML body without contextual encoding.

| Attribute | Value |
|---|---|
| Technology | .NET / C# |
| CWE | CWE-79 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/Program.cs) · [Corrected source](fixed/Program.cs)

## Correction

Encode text for the HTML body context; other contexts need their own encoding.

## Regression

```sh
python3 tools/lab.py test --case dotnet/xss --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| plain text | benign | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} | {"equals": "&lt;p&gt;hello&lt;/p&gt;"} |
| HTML element | attack | {"equals": "&lt;p&gt;&lt;script&gt;alert(1)&lt;/script&gt;&lt;/p&gt;"} | {"equals": "&lt;p&gt;&amp;lt;script&amp;gt;alert(1)&amp;lt;/script&amp;gt;&lt;/p&gt;"} |
| ampersand | attack | {"equals": "&lt;p&gt;a&amp;b&lt;/p&gt;"} | {"equals": "&lt;p&gt;a&amp;amp;b&lt;/p&gt;"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
