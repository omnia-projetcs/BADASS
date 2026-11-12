# Regular expression denial of service (ReDoS)

Nested repetition quantifiers cause exponential backtracking steps when validating a lowercase tag with an invalid trailing character.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-1333 |
| OWASP | A06:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Bound the input length and replace ambiguous nested quantifiers with a linear-time character check.

## Regression

```sh
python3 tools/lab.py test --case python/redos --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid tag | benign | {"equals": {"valid": true, "tag": "release"}} | {"equals": {"valid": true, "tag": "release"}} |
| backtracking suffix payload | attack | {"equals": {"valid": false, "steps": 1024}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
