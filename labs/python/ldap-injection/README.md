# LDAP filter injection

String concatenation in an LDAP search filter permits wildcard and boolean-clause injection to retrieve administrative directory attributes.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-90 |
| OWASP | A05:2025 |
| Test scope | `handler-unit` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Validate username syntax and escape RFC 4515 metacharacters before constructing directory filters.

## Regression

```sh
python3 tools/lab.py test --case python/ldap-injection --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal user lookup | benign | {"equals": "alice@example.test"} | {"equals": "alice@example.test"} |
| filter clause injection | attack | {"equals": "secret-admin@example.test"} | {"equals": "DENIED"} |
| wildcard enumeration | attack | {"equals": "secret-admin@example.test"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
