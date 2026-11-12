# Cryptographic stream-cipher nonce reuse

Reusing a static nonce in a stream cipher produces identical keystreams, allowing XOR recovery of a secret plaintext from a known plaintext.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-323, CWE-329, CWE-327 |
| OWASP | A04:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Generate a unique nonce for every encrypted message and refuse operations that reuse or omit per-message nonces.

## Regression

```sh
python3 tools/lab.py test --case python/crypto-nonce-reuse --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| decrypt public record | benign | {"equals": "PUBLIC_HEADER_16"} | {"equals": "PUBLIC_HEADER_16"} |
| two-time pad XOR recovery | attack | {"equals": "LAB_SECRET_TOKEN"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
