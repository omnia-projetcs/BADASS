# Go

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language go --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Cross-site scripting (XSS)](xss/README.md) | CWE-79 | A05:2025 | executable |
| [Path traversal](path-traversal/README.md) | CWE-22 | A01:2025 | executable |
| [Command injection](command-injection/README.md) | CWE-78 | A05:2025 | executable |
| [SQL injection](sql-injection/README.md) | CWE-89 | A05:2025 | executable |
