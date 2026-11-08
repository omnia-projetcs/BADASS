# ImageTragick: delegate shell injection

Original reduced Python model inspired by CVE-2016-3714. A parsed SVG resource URL is substituted into a shell-based delegate command. A crafted resource writes a real local marker via the shell. The delegate is the local printf utility, never an image converter or downloader, so this exercises the shell boundary without contacting the URL or reproducing ImageMagick.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-78 |
| CVE | CVE-2016-3714 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Pass the parsed resource as one positional argv element to a fixed executable, without a shell. Validate the bounded XML and expected resource scheme before delegation in both variants. The tests use only local printf commands and synthetic files. Real ImageMagick remediation also requires its security fixes and a suitable coder/delegate policy.

## Regression

```sh
python3 tools/lab.py test --case python/imagetragick-delegate --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary SVG resource | benign | {"equals": {"status": 200, "echo": "https://images.test/picture.png"}, "files": [{"path": "delegate-marker", "type": "absent"}]} | {"equals": {"status": 200, "echo": "https://images.test/picture.png"}, "files": [{"path": "delegate-marker", "type": "absent"}]} |
| resource query | benign | {"equals": {"status": 200, "echo": "https://images.test/picture?q=one"}, "files": [{"path": "delegate-marker", "type": "absent"}]} | {"equals": {"status": 200, "echo": "https://images.test/picture?q=one"}, "files": [{"path": "delegate-marker", "type": "absent"}]} |
| quote terminates delegate argument | attack | {"equals": {"status": 200, "echo": "https://images.test/x"}, "files": [{"path": "delegate-marker", "content": "LAB_MARKER"}]} | {"equals": {"status": 200, "echo": "https://images.test/x\"; printf LAB_MARKER &gt; delegate-marker; #"}, "files": [{"path": "delegate-marker", "type": "absent"}]} |
| command substitution in resource | attack | {"equals": {"status": 200, "echo": "https://images.test/x"}, "files": [{"path": "delegate-marker", "content": "LAB_SECOND"}]} | {"equals": {"status": 200, "echo": "https://images.test/x$(printf LAB_SECOND &gt; delegate-marker)"}, "files": [{"path": "delegate-marker", "type": "absent"}]} |
| malformed XML | robustness | {"equals": {"status": 400, "error": "invalid image resource"}} | {"equals": {"status": 400, "error": "invalid image resource"}} |
| wrong resource scheme | robustness | {"equals": {"status": 400, "error": "invalid image resource"}} | {"equals": {"status": 400, "error": "invalid image resource"}} |
| no resource | robustness | {"equals": {"status": 400, "error": "invalid image resource"}} | {"equals": {"status": 400, "error": "invalid image resource"}} |
| wrong document type | robustness | {"equals": {"status": 400, "error": "invalid image resource"}} | {"equals": {"status": 400, "error": "invalid image resource"}} |
| DTD disabled | robustness | {"equals": {"status": 400, "error": "invalid image resource"}} | {"equals": {"status": 400, "error": "invalid image resource"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [ImageTragick original researcher disclosure — CVE-2016-3714](https://imagetragick.com/)
- [EDB-39767 — ImageMagick delegate shell injection](https://www.exploit-db.com/exploits/39767)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
