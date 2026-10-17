# Predictable token

Account-derived reset tokens permit a public guess to authenticate against the actual token store.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-330 |
| OWASP | A07:2025 |
| Test scope | `state-machine-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Issue CSPRNG tokens while preserving issuance, validation and one-time consumption. A trusted observer checks usability, replay rejection, unrelated state and repeated issuance. Finite tests do not certify entropy; this in-memory fixture does not model expiration or concurrent requests.

## Regression

```sh
python3 tools/lab.py test --case python/predictable-token --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

Trusted oracle: `reset_token`. Vector `context` is supplied by the harness outside candidate input.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty account | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| issued token authenticates | benign | {"equals": {"issued_token_usable": true, "wrong_token_rejected": true, "consumed_token_accepted": true, "replay_rejected": true, "token_removed": true, "unrelated_token_preserved": true}} | {"equals": {"issued_token_usable": true, "wrong_token_rejected": true, "consumed_token_accepted": true, "replay_rejected": true, "token_removed": true, "unrelated_token_preserved": true}} |
| public account-derived guess | attack | {"equals": {"issued_token_usable": true, "public_guess_accepted": true}} | {"equals": {"issued_token_usable": true, "public_guess_accepted": false}} |
| repeated issuance changes token | attack | {"equals": {"issued_tokens_usable": true, "distinct_tokens": false}} | {"equals": {"issued_tokens_usable": true, "distinct_tokens": true}} |
| Unicode account remains usable | benign | {"equals": {"issued_token_usable": true, "wrong_token_rejected": true, "consumed_token_accepted": true, "replay_rejected": true, "token_removed": true, "unrelated_token_preserved": true}} | {"equals": {"issued_token_usable": true, "wrong_token_rejected": true, "consumed_token_accepted": true, "replay_rejected": true, "token_removed": true, "unrelated_token_preserved": true}} |
| null account | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |
| structured account | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
