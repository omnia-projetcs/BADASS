# PHP

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language php --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Cross-site scripting (XSS)](xss/README.md) | CWE-79 | A05:2025 | executable |
| [Path traversal](path-traversal/README.md) | CWE-22 | A01:2025 | executable |
| [Command injection](command-injection/README.md) | CWE-78 | A05:2025 | executable |
| [SQL injection](sql-injection/README.md) | CWE-89 | A05:2025 | executable |
| [Insecure direct object reference (IDOR)](idor/README.md) | CWE-639 | A01:2025 | handler-unit |
| [Missing authorization](missing-authorization/README.md) | CWE-862 | A01:2025 | handler-unit |
| [Hardcoded credentials](hardcoded-credentials/README.md) | CWE-798 | A07:2025 | handler-unit |
| [Log injection](log-injection/README.md) | CWE-117 | A09:2025 | executable |
| [Error disclosure](error-disclosure/README.md) | CWE-209 | A02:2025 | handler-unit |
| [Fail open](fail-open/README.md) | CWE-636 | A10:2025 | handler-unit |
| [Open redirect](open-redirect/README.md) | CWE-601 | A01:2025 | handler-unit |
| [Unbounded work](unbounded-work/README.md) | CWE-400 | A06:2025 | executable |
| [Invalid purchase quantity](business-logic/README.md) | CWE-1284 | A06:2025 | handler-unit |
| [World readable secret](world-readable-secret/README.md) | CWE-732 | A01:2025 | executable |
| [HTTP response header injection](header-injection/README.md) | CWE-113 | A05:2025 | handler-unit |
| [Symlink following](symlink-following/README.md) | CWE-59 | A01:2025 | executable |
