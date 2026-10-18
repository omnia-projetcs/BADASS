# Jwt default key

An HS256 JWT verifier silently falls back to a publicly known signing key when deployment configuration is absent. A forged administrator token then passes real HMAC verification. Inspired by the weak-secret pattern described in EDB-51354; this is original Python code, not the affected product.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-321 |
| OWASP | A04:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Require an externally supplied random signing key and fail closed when absent or shorter than 32 bytes. The bounded HS256-only profile also checks the signature, issuer, audience, expiration and not-before fields. BADASS_JWT_KEY values in tests are public synthetic fixtures, not deployment secrets; length is not an entropy test. NOW is a pinned lab clock, not wall time. This is not a general JWT library.

## Regression

```sh
python3 tools/lab.py test --case python/jwt-default-key --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| active alice | benign | {"equals": {"status": 200, "user": "alice", "role": "reader"}} | {"equals": {"status": 200, "user": "alice", "role": "reader"}} |
| active admin | benign | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 200, "user": "admin", "role": "admin"}} |
| wrong signature | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| expired token | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| expiry boundary | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| future token | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| wrong audience | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| wrong issuer | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| unknown account | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| malformed token | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| missing token | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| non-string token | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| non-object request | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| unsupported algorithm | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| boolean expiry | robustness | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |
| forged administrator via default secret | attack | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 503, "error": "signing key unavailable"}} |
| forged reader via default secret | attack | {"equals": {"status": 200, "user": "alice", "role": "reader"}} | {"equals": {"status": 503, "error": "signing key unavailable"}} |
| explicit short key | attack | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 503, "error": "signing key unavailable"}} |
| explicit empty key | attack | {"equals": {"status": 200, "user": "admin", "role": "admin"}} | {"equals": {"status": 503, "error": "signing key unavailable"}} |
| configured key rejects public default | benign | {"equals": {"status": 401, "error": "denied"}} | {"equals": {"status": 401, "error": "denied"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-51354 — ever gauzy v0.281.9 JWT weak HMAC secret — nu11secur1ty](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/typescript/webapps/51354.txt)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
