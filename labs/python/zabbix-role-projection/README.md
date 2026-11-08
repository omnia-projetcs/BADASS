# Zabbix: role projection SQL injection

Original reduced Python model inspired by CVE-2024-42327. An authenticated user.get-like API concatenates requested role projection expressions into a real SQLite query. A scalar subquery retrieves another role's synthetic administrator token despite a bound outer role identifier. The model isolates SQL projection injection, not Zabbix or a full privilege-escalation chain.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-89 |
| CVE | CVE-2024-42327 |
| OWASP | A05:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Map requested projection identifiers through an exact allowlist and keep role identifiers bound. Reject the entire projection when any field is unknown; binding values does not make SQL identifiers safe. Preserve authorized multi-column requests and valid reader tokens. Actual remediation is the Zabbix security update.

## Regression

```sh
python3 tools/lab.py test --case python/zabbix-role-projection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| role name | benign | {"equals": {"status": 200, "role": {"name": "reader"}}} | {"equals": {"status": 200, "role": {"name": "reader"}}} |
| multiple approved columns | benign | {"equals": {"status": 200, "role": {"name": "reader", "roleid": 1}}} | {"equals": {"status": 200, "role": {"name": "reader", "roleid": 1}}} |
| role identifier | benign | {"equals": {"status": 200, "role": {"roleid": 1}}} | {"equals": {"status": 200, "role": {"roleid": 1}}} |
| subquery leaks admin token | attack | {"equals": {"status": 200, "role": {"name": "reader", "leaked": "LAB_ADMIN_TOKEN"}}} | {"equals": {"status": 400, "error": "invalid projection"}} |
| alternate scalar query | attack | {"equals": {"status": 200, "role": {"secret": "LAB_ADMIN_TOKEN"}}} | {"equals": {"status": 400, "error": "invalid projection"}} |
| token column not public | attack | {"equals": {"status": 200, "role": {"token": "LAB_READER_TOKEN"}}} | {"equals": {"status": 400, "error": "invalid projection"}} |
| no API token | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| empty projection | robustness | {"equals": {"status": 400, "error": "invalid projection"}} | {"equals": {"status": 400, "error": "invalid projection"}} |
| non-string projection | robustness | {"equals": {"status": 400, "error": "invalid projection"}} | {"equals": {"status": 400, "error": "invalid projection"}} |
| unknown SQL column | robustness | {"equals": {"status": 400, "error": "invalid projection"}} | {"equals": {"status": 400, "error": "invalid projection"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Zabbix ZBX-25623 / CVE-2024-42327 — user.get SQL injection](https://support.zabbix.com/browse/ZBX-25623)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
