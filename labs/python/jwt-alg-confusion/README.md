# JWT algorithm confusion

The JWT verifier honors caller-controlled 'alg: none' headers and public-key KID selection to accept forged administrative tokens.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-347 |
| OWASP | A04:2025, A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Enforce an explicit server-side algorithm allowlist, reject 'none' and untrusted key identifiers, and verify the HMAC tag in constant time.

## Regression

```sh
python3 tools/lab.py test --case python/jwt-alg-confusion --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| valid HS256 token | benign | {"equals": "alice"} | {"equals": "alice"} |
| alg none bypass | attack | {"equals": "admin"} | {"equals": "DENIED"} |
| public key HMAC confusion | attack | {"equals": "admin"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
