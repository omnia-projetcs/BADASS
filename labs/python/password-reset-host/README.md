# Password reset host

A syntactically valid but untrusted Host controls the origin of a password-reset URL. Inspired by EDB-52485 (CVE-2025-25198). The returned object captures a synthetic email artifact; no email is sent and no HTTP server runs.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-346 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Build reset URLs from a deployment-owned HTTPS origin, independently of Host or forwarded headers. The constant LAB_RESET_TOKEN is only a deterministic observation marker. Token generation, delivery and redemption are outside this fixture; this is not a reproduction of mailcow.

## Regression

```sh
python3 tools/lab.py test --case python/password-reset-host --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| canonical origin | benign | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| forwarded host cannot override configured origin | benign | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| foreign host | attack | {"equals": {"recipient": "alice@example.test", "reset_url": "https://attacker.example.test/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| trusted prefix confusion | attack | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test.attacker.test/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| alternate port | attack | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test:8443/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| loopback origin | attack | {"equals": {"recipient": "alice@example.test", "reset_url": "https://127.0.0.1:8080/reset-password?token=LAB_RESET_TOKEN"}} | {"equals": {"recipient": "alice@example.test", "reset_url": "https://accounts.example.test/reset-password?token=LAB_RESET_TOKEN"}} |
| missing host | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |
| non-object request | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |
| non-string host | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |
| newline host | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |
| userinfo host | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |
| oversized host | robustness | {"equals": {"status": 400, "error": "invalid host"}} | {"equals": {"status": 400, "error": "invalid host"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-52485 — mailcow Host Header Password Reset Poisoning — Iam Alvarez](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/multiple/webapps/52485.txt)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
