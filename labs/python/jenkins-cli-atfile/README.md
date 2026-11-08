# Jenkins CLI: pre-auth file expansion

Original reduced Python model inspired by CVE-2024-23897. A CLI parser expands @file arguments before the command permission check. Its help error exposes the first line of a real synthetic private file. The reduced parser demonstrates pre-authorization disclosure only; it is not args4j, a Jenkins controller or the later RCE chain.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-73 |
| CVE | CVE-2024-23897 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Disable @file expansion for remotely supplied CLI arguments. Keep those arguments literal rather than attempting to authorize after expansion. File expansion in the vulnerable model is bounded to existing files inside the fixture workspace and a small size; it never reads outside the laboratory working directory. Actual Jenkins remediation is upgrading or disabling the affected CLI.

## Regression

```sh
python3 tools/lab.py test --case python/jenkins-cli-atfile --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| anonymous literal argument | benign | {"equals": {"status": 403, "argument": "help"}} | {"equals": {"status": 403, "argument": "help"}} |
| authorized literal arguments | benign | {"equals": {"status": 200, "arguments": ["list", "jobs"]}} | {"equals": {"status": 200, "arguments": ["list", "jobs"]}} |
| anonymous private file | attack | {"equals": {"status": 403, "argument": "LAB_SECRET"}} | {"equals": {"status": 403, "argument": "@secret.txt"}} |
| second private file | attack | {"equals": {"status": 403, "argument": "LAB_SECRET"}} | {"equals": {"status": 403, "argument": "@private.txt"}} |
| authorized parser file expansion | attack | {"equals": {"status": 200, "arguments": ["LAB_SECRET"]}} | {"equals": {"status": 200, "arguments": ["@secret.txt"]}} |
| literal at character inside text | benign | {"equals": {"status": 403, "argument": "user@example.test"}} | {"equals": {"status": 403, "argument": "user@example.test"}} |
| empty args | robustness | {"equals": {"status": 400, "error": "invalid command"}} | {"equals": {"status": 400, "error": "invalid command"}} |
| non-string argument | robustness | {"equals": {"status": 400, "error": "invalid command"}} | {"equals": {"status": 400, "error": "invalid command"}} |
| wrong request | robustness | {"equals": {"status": 400, "error": "invalid command"}} | {"equals": {"status": 400, "error": "invalid command"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Jenkins SECURITY-3314 / CVE-2024-23897 — official advisory](https://www.jenkins.io/security/advisory/2024-01-24/)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
