# Session fixation

Login upgrades an attacker-selected session identifier into a real authenticated session.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-384 |
| OWASP | A07:2025 |
| Test scope | `state-machine-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Remove the pre-login session and issue a fresh identifier that resolves to the authenticated principal. Trusted observers inspect session state, verify real logout and require unrelated sessions and legitimate login to remain functional.

## Regression

```sh
python3 tools/lab.py test --case python/session-fixation --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

Trusted oracle: `session_rotation`. Vector `context` is supplied by the harness outside candidate input.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| legitimate login succeeds | benign | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true}} | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true}} |
| login followed by real logout | benign | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true, "logout_succeeded": true, "logged_out_session_rejected": true, "logged_out_session_removed": true}} | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true, "logout_succeeded": true, "logged_out_session_rejected": true, "logged_out_session_removed": true}} |
| client-selected session is invalidated | attack | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true, "id_rotated": false, "old_session_removed": false, "old_session_authenticated": true}} | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true, "id_rotated": true, "old_session_removed": true, "old_session_authenticated": false}} |
| second trusted principal can log in | benign | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true}} | {"equals": {"new_session_authenticated": true, "unrelated_session_preserved": true}} |
| empty session identifier | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |
| null session identifier | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |
| structured session identifier | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
