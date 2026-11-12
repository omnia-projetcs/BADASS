# MCP tool description poisoning

An MCP tool loader ingests untrusted tool description metadata containing hidden prompt-override directives into the agent instruction context.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-1427 |
| OWASP | LLM01:2025, LLM03:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Allowlist approved tool identifiers, restrict description character sets and length, and reject directive-injection markers in tool metadata.

## Regression

```sh
python3 tools/lab.py test --case ai/mcp-tool-poisoning --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| clean MCP tool registration | benign | {"equals": {"registered": true, "tool": "search_docs"}} | {"equals": {"registered": true, "tool": "search_docs"}} |
| poisoned tool description directive | attack | {"equals": {"registered": true, "effect": "POLICY_OVERRIDDEN"}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
