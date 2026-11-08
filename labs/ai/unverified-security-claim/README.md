# Unverified security claim

A generated claim closes a security finding without independent evidence.

| Attribute | Value |
|---|---|
| Technology | AI / LLM boundaries |
| CWE | CWE-345 |
| OWASP | LLM09:2025 |
| Test scope | `ai-boundary-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Accept a resolved claim only when the application supplies a nonempty independent regression report with all checks passed and the digest of the exact reviewed artifact. Evidence embedded in model output is untrusted; absent, skipped, failed or stale evidence leaves the finding open.

## Regression

```sh
python3 tools/lab.py test --case ai/unverified-security-claim --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

Trusted oracle: `security_claim`. Vector `context` is supplied by the harness outside candidate input.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| unresolved claim | benign | {"equals": "OPEN"} | {"equals": "OPEN"} |
| independently verified current artifact | benign | {"equals": "CLOSED"} | {"equals": "CLOSED"} |
| unsupported resolution | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| empty regression | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| skipped check | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| failed check | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| stale artifact | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| malformed check | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| model supplies its own evidence | attack | {"equals": "CLOSED"} | {"equals": "OPEN"} |
| malformed trusted digest | robustness | {"equals": "CLOSED"} | {"equals": "OPEN"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
