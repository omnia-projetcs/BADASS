# Weak password hash

Working password records use unsalted fast MD5 in the vulnerable variant.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-916 |
| OWASP | A04:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Store an explicit salted scrypt record and verify passwords against persisted records. The trusted oracle independently recomputes the fixture profile (n=16384, r=8, p=1, 32-byte key); calibrate a production policy separately.

## Regression

```sh
python3 tools/lab.py test --case python/weak-password-hash --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

Trusted oracle: `password_hash`. Vector `context` is supplied by the harness outside candidate input.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty password | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| stored password works and wrong password fails | benign | {"equals": {"correct_password_works": true, "wrong_password_rejected": true}} | {"equals": {"correct_password_works": true, "wrong_password_rejected": true}} |
| independent verification of stored KDF | attack | {"equals": {"correct_password_works": true, "valid_scrypt_record": false}} | {"equals": {"correct_password_works": true, "valid_scrypt_record": true}} |
| separate password records use separate salts | attack | {"equals": {"records_usable": true, "distinct_salts": false, "distinct_digests": false}} | {"equals": {"records_usable": true, "distinct_salts": true, "distinct_digests": true}} |
| Unicode password round trip | benign | {"equals": {"correct_password_works": true, "wrong_password_rejected": true}} | {"equals": {"correct_password_works": true, "wrong_password_rejected": true}} |
| null password | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |
| structured password | robustness | {"equals": "DENIED"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
