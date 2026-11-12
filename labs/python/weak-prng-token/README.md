# Weak PRNG token generation

Seeding the non-cryptographic Mersenne Twister PRNG with a predictable timestamp allows an attacker to compute subsequent administrative session tokens.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-338 |
| OWASP | A04:2025, A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Generate security tokens exclusively with a cryptographically secure random number generator (secrets.token_hex) and compare in constant time.

## Regression

```sh
python3 tools/lab.py test --case python/weak-prng-token --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| service health check | benign | {"equals": "OK"} | {"equals": "OK"} |
| predicted PRNG admin token | attack | {"equals": "ADMIN_SESSION"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
