# XSS in an HTML attribute

An encoder suitable for an HTML text node leaves quotes able to inject an event-handler attribute.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-79 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Use a quoted HTML attribute and encode quotes, ampersands and markup characters for that context; verify the parsed attribute structure.

## Regression

```sh
python3 tools/lab.py test --case python/xss-attribute --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary value | benign | {"equals": "&lt;input value=\"Alice\"&gt;"} | {"equals": "&lt;input value=\"Alice\"&gt;"} |
| markup characters remain text | benign | {"equals": "&lt;input value=\"Alice &amp;amp; Bob &amp;lt;team&amp;gt;\"&gt;"} | {"equals": "&lt;input value=\"Alice &amp;amp; Bob &amp;lt;team&amp;gt;\"&gt;"} |
| focus event attribute | attack | {"equals": "&lt;input value=\"\" autofocus onfocus=\"window.LAB_MARKER=1\"&gt;"} | {"equals": "&lt;input value=\"&amp;quot; autofocus onfocus=&amp;quot;window.LAB_MARKER=1\"&gt;"} |
| pointer event attribute | attack | {"equals": "&lt;input value=\"x\" onmouseover=\"window.LAB_MARKER=2\"&gt;"} | {"equals": "&lt;input value=\"x&amp;quot; onmouseover=&amp;quot;window.LAB_MARKER=2\"&gt;"} |
| apostrophe text is preserved by HTML parsing | functional | {"equals": "&lt;input value=\"O'Reilly\"&gt;"} | {"equals": "&lt;input value=\"O&amp;#x27;Reilly\"&gt;"} |
| attribute must be a string | robustness | {"equals": {"status": 400, "error": "invalid value"}} | {"equals": {"status": 400, "error": "invalid value"}} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
