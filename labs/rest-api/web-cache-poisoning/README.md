# Web cache poisoning

An unkeyed X-Forwarded-Host header is reflected into a cached response and served to subsequent visitors requesting the same path.

| Attribute | Value |
|---|---|
| Technology | REST API (Python handlers) |
| CWE | CWE-525, CWE-444 |
| OWASP | A02:2025, API8:2023 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject untrusted forwarding headers and construct cached asset URLs exclusively from the canonical server-configured origin.

## Regression

```sh
python3 tools/lab.py test --case rest-api/web-cache-poisoning --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal cached page | benign | {"equals": "&lt;script src='https://app.example.test/bundle.js'&gt;&lt;/script&gt;"} | {"equals": "&lt;script src='https://app.example.test/bundle.js'&gt;&lt;/script&gt;"} |
| poisoned X-Forwarded-Host cache hit | attack | {"equals": "&lt;script src='https://attacker.invalid/bundle.js'&gt;&lt;/script&gt;"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
