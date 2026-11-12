# Memory poisoning

Untrusted retrieval output writes directly to the agent's persistent memory store and overwrites the security_policy key for future sessions.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-472 |
| OWASP | LLM04:2025, LLM01:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Verify trusted provenance before persisting memory updates and restrict mutable keys and values to an explicit preference allowlist.

## Regression

```sh
python3 tools/lab.py test --case ai/memory-poisoning --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| trusted theme preference update | benign | {"equals": {"theme": "dark", "security_policy": "strict"}} | {"equals": {"theme": "dark", "security_policy": "strict"}} |
| untrusted retrieval policy overwrite | attack | {"equals": {"theme": "light", "security_policy": "disabled"}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
