# GitLab: unverified reset recipients

Original reduced Python model inspired by CVE-2023-7028. A reset request identifies a real account from one verified address but delivers the same recovery token to every supplied address, including an unverified recipient. Tests inspect a real synthetic outbox file. SMTP, password changes and GitLab application code are outside this model.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-640 |
| CVE | CVE-2023-7028 |
| OWASP | A07:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Resolve exactly one account and filter delivery recipients against its server-side verified addresses. Preserve valid secondary addresses and reject requests spanning multiple accounts. The token is a fixed laboratory marker so tests isolate recipient authorization, not token generation security. Real remediation requires the GitLab security update.

## Regression

```sh
python3 tools/lab.py test --case python/gitlab-reset-recipients --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| verified primary address | benign | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} |
| verified secondary address | benign | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice.alt@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice.alt@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} |
| unknown address | benign | {"equals": {"status": 202, "queued": 0}, "files": [{"path": "outbox.json", "type": "absent"}]} | {"equals": {"status": 202, "queued": 0}, "files": [{"path": "outbox.json", "type": "absent"}]} |
| extra unverified recipient | attack | {"equals": {"status": 202, "queued": 2}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}, {\"to\": \"attacker@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} |
| unverified recipient first | attack | {"equals": {"status": 202, "queued": 2}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"attacker@example.test\", \"token\": \"LAB_RESET_TOKEN\"}, {\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} |
| verified address deduplication | benign | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} | {"equals": {"status": 202, "queued": 1}, "files": [{"path": "outbox.json", "content": "[{\"to\": \"alice@example.test\", \"token\": \"LAB_RESET_TOKEN\"}]\n"}]} |
| ambiguous account request | robustness | {"equals": {"status": 400, "error": "invalid recovery request"}} | {"equals": {"status": 400, "error": "invalid recovery request"}} |
| empty recipient list | robustness | {"equals": {"status": 400, "error": "invalid recovery request"}} | {"equals": {"status": 400, "error": "invalid recovery request"}} |
| mail header injection | robustness | {"equals": {"status": 400, "error": "invalid recovery request"}} | {"equals": {"status": 400, "error": "invalid recovery request"}} |
| wrong recipient type | robustness | {"equals": {"status": 400, "error": "invalid recovery request"}} | {"equals": {"status": 400, "error": "invalid recovery request"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [GitLab CNA record for CVE-2023-7028 — unverified recovery email](https://gitlab.com/gitlab-org/cves/-/blob/40bb099b1d6622fad9a67a2ed4e4c7addc9388a2/2023/CVE-2023-7028.json)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
