# Jwt disabled user

An otherwise valid signed JWT continues to authorize a disabled account because the handler checks only account existence. Inspired by the inactive-user scenario in EDB-51992. The fixed handler consults current server-owned account state on every request.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-863 |
| OWASP | A01:2025, A07:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Verify the token cryptographically and require the current account to exist and be active before using its server-owned role. The token cannot override account activation or role. Tests use a bounded HS256 profile, a pinned clock, an in-memory account store and a synthetic external key; they do not reproduce Django or certify a third-party advisory.

## Regression

```sh
python3 tools/lab.py test --case python/jwt-disabled-user --strict
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
| disabled account with signed token | attack | {"equals": {"status": 200, "user": "bob", "role": "reader"}} | {"equals": {"status": 401, "error": "denied"}} |
| token cannot reenable account | attack | {"equals": {"status": 200, "user": "bob", "role": "reader"}} | {"equals": {"status": 401, "error": "denied"}} |
| token cannot elevate active user role | benign | {"equals": {"status": 200, "user": "alice", "role": "reader"}} | {"equals": {"status": 200, "user": "alice", "role": "reader"}} |
| missing signing key fails closed | robustness | {"equals": {"status": 503, "error": "signing key unavailable"}} | {"equals": {"status": 503, "error": "signing key unavailable"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [EDB-51992 — djangorestframework-simplejwt inactive-user scenario — Dhrumil Mistry](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/python/webapps/51992.py)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
