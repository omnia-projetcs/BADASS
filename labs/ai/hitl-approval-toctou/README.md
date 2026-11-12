# HITL approval TOCTOU bypass

An agent mutates tool arguments between human-in-the-loop preview approval and actual execution because approval is keyed only by action_id.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-367 |
| OWASP | LLM06:2025, A01:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Cryptographically bind the human approval digest to the exact action identifier, recipient, and amount before executing the tool.

## Regression

```sh
python3 tools/lab.py test --case ai/hitl-approval-toctou --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| matching preview and execution | benign | {"equals": {"executed": true, "recipient": "alice", "amount": 25}} | {"equals": {"executed": true, "recipient": "alice", "amount": 25}} |
| mutated recipient and amount after approval | attack | {"equals": {"executed": true, "recipient": "attacker", "amount": 900}} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
