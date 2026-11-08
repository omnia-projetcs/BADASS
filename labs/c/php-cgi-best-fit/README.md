# PHP-CGI best-fit argument injection

An original C model of the Windows PHP-CGI best-fit argument boundary. A percent-encoded soft-hyphen byte becomes a dash after the CGI option guard, activating an internal synthetic include_private option. A real getopt parser consumes the resulting argv. No PHP runtime, Windows codepage API, script or system command is executed.

| Attribute | Value |
|---|---|
| Technology | C |
| CWE | CWE-88 |
| CVE | CVE-2024-4577 |
| OWASP | A05:2025 |
| Test scope | `native-model` |

[Vulnerable source](vulnerable/main.c) · [Corrected source](fixed/main.c)

## Correction

Normalize with the same byte mapping used by the option consumer before checking a dash-prefixed query. Preserve normal key/value query handling, reject malformed encodings and unsupported bytes, and limit the synthetic option to a fixed private-data marker. This models the best-fit bypass only; actual CVE remediation requires a corrected PHP-CGI runtime for the relevant Windows deployment.

## Regression

```sh
python3 tools/lab.py test --case c/php-cgi-best-fit --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| normal search query | benign | {"equals": "PUBLIC"} | {"equals": "PUBLIC"} |
| query without assignment | benign | {"equals": "PUBLIC"} | {"equals": "PUBLIC"} |
| empty query | benign | {"equals": "PUBLIC"} | {"equals": "PUBLIC"} |
| ordinary dash already blocked | benign | {"equals": "DENIED"} | {"equals": "DENIED"} |
| soft hyphen injected option | attack | {"equals": "LAB_PRIVATE_CONFIG"} | {"equals": "DENIED"} |
| case insensitive encoded byte | attack | {"equals": "LAB_PRIVATE_CONFIG"} | {"equals": "DENIED"} |
| leading encoded spaces | attack | {"equals": "LAB_PRIVATE_CONFIG"} | {"equals": "DENIED"} |
| encoded option inside value is data | benign | {"equals": "PUBLIC"} | {"equals": "PUBLIC"} |
| truncated escape | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| invalid escape | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| NUL escape | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |
| oversized query | robustness | {"equals": "INVALID"} | {"equals": "INVALID"} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2024-4577 — argument injection advisory](https://github.com/php/php-src/security/advisories/GHSA-3qgc-jrrr-25jv)
- [EDB-52331 — PHP CGI Module argument injection](https://www.exploit-db.com/exploits/52331)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
