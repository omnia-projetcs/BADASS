# Cross tenant retrieval

Vector retrieval returns documents from another tenant.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-863 |
| OWASP | LLM08:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Apply tenant authorization before returning retrieval results.

## Regression

```sh
python3 tools/lab.py test --case ai/cross-tenant-retrieval --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| own document | benign | {"equals": ["ALICE_PUBLIC"]} | {"equals": ["ALICE_PUBLIC"]} |
| other tenant | attack | {"equals": ["BOB_PRIVATE"]} | {"equals": []} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
