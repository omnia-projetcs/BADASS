# Spring4Shell: class-loader property binding

Original reduced Python model inspired by CVE-2022-22965. A dotted-property binder traverses a synthetic class/module/class-loader graph and changes an internal access-log prefix. The sink writes a real local log to the altered filename. It models the binding boundary, not Spring, Tomcat, JSP writing or RCE.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-915 |
| CVE | CVE-2022-22965 |
| OWASP | A01:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Preflight an exact allowlist of client-editable properties, including an explicitly allowed nested profile field, before traversing or modifying the model. Log prefixes remain confined to a synthetic logs directory in both variants. Actual Spring remediation requires the vendor fix and consideration of the deployment prerequisites described in its advisory.

## Regression

```sh
python3 tools/lab.py test --case python/spring4shell-binding --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary form | benign | {"equals": {"status": 200, "name": "bob", "display_name": "Alice"}, "files": [{"path": "logs/access.log", "content": "user=bob\n"}]} | {"equals": {"status": 200, "name": "bob", "display_name": "Alice"}, "files": [{"path": "logs/access.log", "content": "user=bob\n"}]} |
| allowed nested profile | benign | {"equals": {"status": 200, "name": "alice", "display_name": "Alicia"}, "files": [{"path": "logs/access.log", "content": "user=alice\n"}]} | {"equals": {"status": 200, "name": "alice", "display_name": "Alicia"}, "files": [{"path": "logs/access.log", "content": "user=alice\n"}]} |
| empty form | benign | {"equals": {"status": 200, "name": "alice", "display_name": "Alice"}, "files": [{"path": "logs/access.log", "content": "user=alice\n"}]} | {"equals": {"status": 200, "name": "alice", "display_name": "Alice"}, "files": [{"path": "logs/access.log", "content": "user=alice\n"}]} |
| class-loader traversal | attack | {"equals": {"status": 200, "name": "alice", "display_name": "Alice"}, "files": [{"path": "logs/private.log", "content": "user=alice\n"}]} | {"equals": {"status": 400, "error": "invalid binding"}, "files": [{"path": "logs/private.log", "type": "absent"}, {"path": "logs/access.log", "type": "absent"}]} |
| whole binding preflight | attack | {"equals": {"status": 200, "name": "bob", "display_name": "Alice"}, "files": [{"path": "logs/changed.log", "content": "user=bob\n"}]} | {"equals": {"status": 400, "error": "invalid binding"}} |
| unknown property | robustness | {"equals": {"status": 400, "error": "invalid binding"}} | {"equals": {"status": 400, "error": "invalid binding"}} |
| non-string value | robustness | {"equals": {"status": 400, "error": "invalid binding"}} | {"equals": {"status": 400, "error": "invalid binding"}} |
| wrong request type | robustness | {"equals": {"status": 400, "error": "invalid binding"}} | {"equals": {"status": 400, "error": "invalid binding"}} |
| path-shaped prefix rejected | benign | {"equals": {"status": 400, "error": "invalid binding"}} | {"equals": {"status": 400, "error": "invalid binding"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Spring Framework CVE-2022-22965 — data-binding RCE advisory](https://spring.io/security/cve-2022-22965/)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
