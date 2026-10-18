# Python

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language python --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Cross-site scripting (XSS)](xss/README.md) | CWE-79 | A05:2025 | executable |
| [Path traversal](path-traversal/README.md) | CWE-22 | A01:2025 | executable |
| [Command injection](command-injection/README.md) | CWE-78 | A05:2025 | executable |
| [SQL injection](sql-injection/README.md) | CWE-89 | A05:2025 | executable |
| [Code injection](code-injection/README.md) | CWE-95 | A05:2025 | executable |
| [Unsafe deserialization](unsafe-deserialization/README.md) | CWE-502 | A08:2025 | executable |
| [Insecure direct object reference (IDOR)](idor/README.md) | CWE-639 | A01:2025 | executable |
| [Mass assignment](mass-assignment/README.md) | CWE-915 | A01:2025 | executable |
| [Cross-site request forgery (CSRF)](csrf/README.md) | CWE-352 | A01:2025 | handler-unit |
| [Session fixation](session-fixation/README.md) | CWE-384 | A07:2025 | state-machine-unit |
| [Weak password hash](weak-password-hash/README.md) | CWE-916 | A04:2025 | executable |
| [Hardcoded credentials](hardcoded-credentials/README.md) | CWE-798 | A07:2025 | executable |
| [Predictable token](predictable-token/README.md) | CWE-330 | A07:2025 | state-machine-unit |
| [Log injection](log-injection/README.md) | CWE-117 | A09:2025 | executable |
| [Sensitive logging](sensitive-logging/README.md) | CWE-532 | A09:2025 | executable |
| [Error disclosure](error-disclosure/README.md) | CWE-209 | A02:2025 | executable |
| [Fail open](fail-open/README.md) | CWE-636 | A10:2025 | executable |
| [Unverified update](unverified-update/README.md) | CWE-494 | A08:2025 | executable |
| [Untrusted plugin](untrusted-plugin/README.md) | CWE-829 | A03:2025 | executable |
| [Open redirect](open-redirect/README.md) | CWE-601 | A01:2025 | executable |
| [Unbounded work](unbounded-work/README.md) | CWE-400 | A06:2025 | executable |
| [Invalid purchase quantity](business-logic/README.md) | CWE-1284 | A06:2025 | executable |
| [World readable secret](world-readable-secret/README.md) | CWE-732 | A01:2025 | executable |
| [Disabled TLS verification](tls-verification/README.md) | CWE-295 | A04:2025 | configuration-unit |
| [Missing security audit events](missing-audit/README.md) | CWE-778 | A09:2025 | handler-unit |
| [Missing authorization](missing-authorization/README.md) | CWE-862 | A01:2025 | handler-unit |
| [HTTP response header injection](header-injection/README.md) | CWE-113 | A05:2025 | handler-unit |
| [Symlink following](symlink-following/README.md) | CWE-59 | A01:2025 | executable |
| [SQL injection in an ORDER BY identifier](sql-order-by/README.md) | CWE-89 | A05:2025 | executable |
| [Second-order SQL injection](sql-second-order/README.md) | CWE-89 | A05:2025 | executable |
| [XSS in an HTML attribute](xss-attribute/README.md) | CWE-79 | A05:2025 | executable |
| [Sql login bypass](sql-login-bypass/README.md) | CWE-89 | A05:2025 | executable |
| [Zip slip](zip-slip/README.md) | CWE-22 | A01:2025 | executable |
| [Password reset host](password-reset-host/README.md) | CWE-346 | A07:2025 | executable |
| [Unrestricted upload](unrestricted-upload/README.md) | CWE-434 | A06:2025 | executable |
| [XML external entities (XXE)](xxe/README.md) | CWE-611 | A02:2025 | executable |
| [Jwt default key](jwt-default-key/README.md) | CWE-321 | A04:2025 | executable |
| [Jwt disabled user](jwt-disabled-user/README.md) | CWE-863 | A01:2025, A07:2025 | executable |
| [Csv formula injection](csv-formula-injection/README.md) | CWE-1236 | A05:2025 | executable |
| [Argument injection](argument-injection/README.md) | CWE-88 | A05:2025 | executable |
| [Format string disclosure](format-string-disclosure/README.md) | CWE-134 | A05:2025 | executable |
| [File create race](file-create-race/README.md) | CWE-367 | A06:2025 | executable |
| [Json parser conflict](json-parser-conflict/README.md) | CWE-436 | A06:2025 | executable |
| [Unicode path validation](unicode-path-validation/README.md) | CWE-180 | A05:2025 | executable |
| [Password reset replay](password-reset-replay/README.md) | CWE-640 | A07:2025 | executable |
| [Webhook signature](webhook-signature/README.md) | CWE-347 | A04:2025 | executable |
| [Decompression amplification](decompression-amplification/README.md) | CWE-409 | A06:2025 | executable |
| [Session expiration](session-expiration/README.md) | CWE-613 | A07:2025 | executable |
