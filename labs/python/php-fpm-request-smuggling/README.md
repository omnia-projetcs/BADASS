# PHP-FPM: persistent FastCGI request smuggling

An original Python handler model of PHP-FPM FastCGI request smuggling on persistent connections. When an application reads only a prefix of the request body and the worker does not drain remaining bytes, the unread body tail is parsed as a second FastCGI request with an attacker-chosen script name. No FastCGI daemon or network socket is used.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-444 |
| CVE | CVE-2026-129289 |
| OWASP | A06:2025, A10:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Unconditionally drain or discard all remaining request-body bytes up to Content-Length (or close the backend connection) before reading the next FastCGI frame. Real PHP-FPM deployments require upgrading to PHP 8.2.36, 8.3.37, 8.4.28, 8.5.13 or 8.6.0 and disabling connection reuse as an interim mitigation.

## Regression

```sh
python3 tools/lab.py test --case python/php-fpm-request-smuggling --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| single request fully read | benign | {"equals": {"status": 200, "executed": ["/var/www/index.php"]}} | {"equals": {"status": 200, "executed": ["/var/www/index.php"]}} |
| two sequential requests on reused connection | benign | {"equals": {"status": 200, "executed": ["/var/www/a.php", "/var/www/b.php"]}} | {"equals": {"status": 200, "executed": ["/var/www/a.php", "/var/www/b.php"]}} |
| unread body tail smuggles second script | attack | {"equals": {"status": 200, "executed": ["/var/www/public.php", "/var/www/admin.php"]}, "files": [{"path": "fpm-executed.log", "content": "/var/www/public.php\n/var/www/admin.php\n"}]} | {"equals": {"status": 200, "executed": ["/var/www/public.php"]}, "files": [{"path": "fpm-executed.log", "content": "/var/www/public.php\n"}]} |
| malformed fastcgi header | robustness | {"equals": {"status": 400, "error": "malformed fastcgi frame"}} | {"equals": {"status": 400, "error": "malformed fastcgi frame"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [PHP CVE-2026-129289 — PHP-FPM FastCGI request smuggling](https://www.php.net/archive/2026.php)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
