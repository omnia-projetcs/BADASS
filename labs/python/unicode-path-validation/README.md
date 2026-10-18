# Unicode path validation

A public-file reader validates the raw filename before applying Unicode NFKC normalization. Compatibility characters become traversal syntax after the check, so the actual file read escapes the public directory.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-180 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Normalize once before validation, enforce a single-component filename policy, resolve the destination and verify containment, then read exactly that checked path. Preserve ordinary and compatible public names. Parent directories are fixture-owned and stable; concurrent filesystem mutation is outside this case.

## Regression

```sh
python3 tools/lab.py test --case python/unicode-path-validation --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary public file | benign | {"equals": {"status": 200, "text": "WELCOME"}} | {"equals": {"status": 200, "text": "WELCOME"}} |
| compatible fullwidth filename | benign | {"equals": {"status": 200, "text": "WELCOME"}} | {"equals": {"status": 200, "text": "WELCOME"}} |
| missing file | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| ordinary Unicode filename | benign | {"equals": {"status": 404}} | {"equals": {"status": 404}} |
| fullwidth traversal | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400}} |
| small full stops | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400}} |
| alternate private target | attack | {"equals": {"status": 200, "text": "LAB_SECRET"}} | {"equals": {"status": 400}} |
| literal traversal | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| empty name | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| non-string name | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| NUL byte | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| current directory | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| backslash path | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |
| oversized name | robustness | {"equals": {"status": 400}} | {"equals": {"status": 400}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-180 — Validate Before Canonicalize](https://cwe.mitre.org/data/definitions/180.html)
- [Python Unicode normalization](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
