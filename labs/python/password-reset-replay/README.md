# Password reset replay

An unpredictable expiring password-reset token remains usable after a successful password change. Replaying it replaces the account password again. The fixture stores token hashes and salted PBKDF2 password hashes in SQLite and observes actual password verification.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-640 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Consume the token in the same database transaction as the password update, under a write lock, and reject unknown, expired or consumed tokens. Roll back both changes if the account write fails. Synthetic times and token selectors belong to the test harness; token delivery, session revocation and production password policy are outside scope.

## Regression

```sh
python3 tools/lab.py test --case python/password-reset-replay --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| first use | benign | {"equals": {"statuses": [200], "password_matches": [true], "initial_password_works": false}} | {"equals": {"statuses": [200], "password_matches": [true], "initial_password_works": false}} |
| last valid instant | benign | {"equals": {"statuses": [200], "password_matches": [true], "initial_password_works": false}} | {"equals": {"statuses": [200], "password_matches": [true], "initial_password_works": false}} |
| replay changes password | attack | {"equals": {"statuses": [200, 200], "password_matches": [false, true], "initial_password_works": false}} | {"equals": {"statuses": [200, 403], "password_matches": [true, false], "initial_password_works": false}} |
| identical password still consumes token | attack | {"equals": {"statuses": [200, 200], "password_matches": [true, true], "initial_password_works": false}} | {"equals": {"statuses": [200, 403], "password_matches": [true, true], "initial_password_works": false}} |
| multiple replays | attack | {"equals": {"statuses": [200, 200, 200], "password_matches": [false, false, true], "initial_password_works": false}} | {"equals": {"statuses": [200, 403, 403], "password_matches": [true, false, false], "initial_password_works": false}} |
| unknown token then valid token | benign | {"equals": {"statuses": [403, 200], "password_matches": [false, true], "initial_password_works": false}} | {"equals": {"statuses": [403, 200], "password_matches": [false, true], "initial_password_works": false}} |
| expired token | benign | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} |
| expiry boundary | benign | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} |
| unknown token | benign | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} | {"equals": {"statuses": [403], "password_matches": [false], "initial_password_works": true}} |
| empty attempt list | robustness | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} |
| malformed request | robustness | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} |
| short password | robustness | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} |
| boolean clock | robustness | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} |
| too many attempts | robustness | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "recovery.sqlite", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-640 — Weak Password Recovery Mechanism](https://cwe.mitre.org/data/definitions/640.html)
- [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
