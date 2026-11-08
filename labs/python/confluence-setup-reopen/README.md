# Confluence: setup-state binding

Original reduced Python model inspired by CVE-2023-22515. An internal setup-complete property is writable through a public binding path. A second request then enters the setup administrator handler and commits an unauthorized account to SQLite. This reduced stateful model is separate from the earlier Confluence expression-injection case.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-915 |
| CVE | CVE-2023-22515 |
| OWASP | A01:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Reject externally supplied internal setup properties and keep setup state in trusted storage. The setup route still supports legitimate initial installation using a server-controlled fresh-install fixture setting. The test environment flag is not client request data. Actual remediation is the patched Confluence release; this is not its Java or HTTP implementation.

## Regression

```sh
python3 tools/lab.py test --case python/confluence-setup-reopen --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| installed server info | benign | {"equals": {"status": 200, "results": [{"status": 200, "setup_complete": true}]}} | {"equals": {"status": 200, "results": [{"status": 200, "setup_complete": true}]}} |
| installed setup route closed | benign | {"equals": {"status": 200, "results": [{"status": 403, "error": "setup closed"}]}} | {"equals": {"status": 200, "results": [{"status": 403, "error": "setup closed"}]}} |
| legitimate initial setup | benign | {"equals": {"status": 200, "results": [{"status": 201, "created": "lab-user"}]}} | {"equals": {"status": 200, "results": [{"status": 201, "created": "lab-user"}]}} |
| public binding reopens setup | attack | {"equals": {"status": 200, "results": [{"status": 200, "setup_complete": false}, {"status": 201, "created": "lab-user"}]}} | {"equals": {"status": 200, "results": [{"status": 403, "error": "protected property"}, {"status": 403, "error": "setup closed"}]}} |
| reopened state visible next request | attack | {"equals": {"status": 200, "results": [{"status": 200, "setup_complete": false}, {"status": 200, "setup_complete": false}]}} | {"equals": {"status": 200, "results": [{"status": 403, "error": "protected property"}, {"status": 200, "setup_complete": true}]}} |
| empty sequence | robustness | {"equals": {"status": 400, "error": "invalid setup request"}} | {"equals": {"status": 400, "error": "invalid setup request"}} |
| wrong property type | robustness | {"equals": {"status": 400, "error": "invalid setup request"}} | {"equals": {"status": 400, "error": "invalid setup request"}} |
| bad username | robustness | {"equals": {"status": 400, "error": "invalid setup request"}} | {"equals": {"status": 400, "error": "invalid setup request"}} |
| wrong request type | robustness | {"equals": {"status": 400, "error": "invalid setup request"}} | {"equals": {"status": 400, "error": "invalid setup request"}} |
| non-string route | robustness | {"equals": {"status": 400, "error": "invalid setup request"}} | {"equals": {"status": 400, "error": "invalid setup request"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Atlassian CVE-2023-22515 — broken access control advisory](https://confluence.atlassian.com/security/cve-2023-22515-broken-access-control-vulnerability-in-confluence-data-center-and-server-1295682276.html)
- [EDB-51829 — Confluence setup authentication bypass](https://www.exploit-db.com/exploits/51829)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
