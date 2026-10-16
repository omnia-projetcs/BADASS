# CGI (Python)

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language cgi --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Cross-site scripting (XSS)](xss/README.md) | CWE-79 | A05:2025 | executable |
| [HTTP response header injection](header-injection/README.md) | CWE-113 | A05:2025 | executable |
