# Session expiration

A server-side session record contains expiry and revocation state, but access checks only that the token exists. The same token can still retrieve a private SQLite report after expiry or a committed logout.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-613 |
| OWASP | A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Check expiry and revocation on every authenticated operation before reading protected data. Persist logout revocation and reject at the exact expiry boundary. The harness uses unpredictable tokens stored as hashes and a synthetic monotonic clock. In-flight requests racing with logout, cookie transport, renewal and idle timeouts are outside scope.

## Regression

```sh
python3 tools/lab.py test --case python/session-expiration --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| active session | benign | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} |
| repeated active reads | benign | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}, {"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}, {"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} |
| last valid instant | benign | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} |
| logout succeeds | benign | {"equals": {"events": [{"status": 204}]}} | {"equals": {"events": [{"status": 204}]}} |
| unknown session | benign | {"equals": {"events": [{"status": 401}]}} | {"equals": {"events": [{"status": 401}]}} |
| unknown logout leaves issued session active | benign | {"equals": {"events": [{"status": 401}, {"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 401}, {"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} |
| expired session | attack | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 401}]}} |
| exact expiry boundary | attack | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 401}]}} |
| read after logout | attack | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}, {"status": 204}, {"status": 200, "report": "LAB_PRIVATE_REPORT"}]}} | {"equals": {"events": [{"status": 200, "report": "LAB_PRIVATE_REPORT"}, {"status": 204}, {"status": 401}]}} |
| empty actions | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| unknown operation | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| boolean clock | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| backwards clock | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| missing token | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| too many actions | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |
| non-object request | robustness | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} | {"equals": {"status": 400}, "files": [{"path": "sessions.sqlite", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-613 — Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
