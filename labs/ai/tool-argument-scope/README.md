# Tool argument scope

An operator-issued report tool accepts model arguments that write outside its allowed report destinations into synthetic source configuration.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-863 |
| OWASP | A01:2025, LLM06:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Authorize both the tool and normalized destination against server-owned capabilities before writing; model scope claims cannot grant rights and fixture parents remain trusted.

## Regression

```sh
python3 tools/lab.py test --case ai/tool-argument-scope --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| write the findings report | benign | {"equals": {"status": "written", "path": "reports/findings.txt", "bytes": 25}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "Checked 3 synthetic files"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} | {"equals": {"status": "written", "path": "reports/findings.txt", "bytes": 25}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "Checked 3 synthetic files"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| write the summary report | benign | {"equals": {"status": "written", "path": "reports/summary.txt", "bytes": 27}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "Audit synthetic code: café"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} | {"equals": {"status": "written", "path": "reports/summary.txt", "bytes": 27}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "Audit synthetic code: café"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| allowed tool cannot overwrite source configuration | attack | {"equals": {"status": "written", "path": "source/settings.txt", "bytes": 12}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_TAMPERED"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| model scope and role do not expand operator capability | attack | {"equals": {"status": "written", "path": "source/settings.txt", "bytes": 12}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_TAMPERED"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| unissued report destination is refused | attack | {"equals": {"status": "written", "path": "reports/unapproved.txt", "bytes": 12}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}, {"path": "reports/unapproved.txt", "type": "file", "content": "LAB_TAMPERED"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}, {"path": "reports/unapproved.txt", "type": "absent"}]} |
| unknown tool is denied | robustness | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| traversal remains outside the allowed workspace | robustness | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |
| tool arguments must be an object | robustness | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} | {"equals": {"status": "denied"}, "files": [{"path": "reports/findings.txt", "type": "file", "content": "DRAFT_FINDINGS"}, {"path": "reports/summary.txt", "type": "file", "content": "DRAFT_SUMMARY"}, {"path": "source/settings.txt", "type": "file", "content": "LAB_SERVER_CONFIG"}]} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
