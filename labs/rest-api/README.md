# REST API (Python handlers)

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language rest-api --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Broken object-level authorization (BOLA)](bola/README.md) | CWE-639 | API1:2023 | handler-unit |
| [Broken authentication](broken-authentication/README.md) | CWE-287 | API2:2023 | handler-unit |
| [Property authorization](property-authorization/README.md) | CWE-915 | API3:2023 | handler-unit |
| [Resource consumption](resource-consumption/README.md) | CWE-770 | API4:2023 | handler-unit |
| [Function authorization](function-authorization/README.md) | CWE-862 | API5:2023 | handler-unit |
| [Business flow abuse](business-flow-abuse/README.md) | CWE-799 | API6:2023 | state-machine-unit |
| [Server-side request forgery (SSRF)](ssrf/README.md) | CWE-918 | API7:2023 | loopback-integration |
| [Credentialed CORS misconfiguration](cors-misconfiguration/README.md) | CWE-942 | API8:2023 | handler-unit |
| [Legacy endpoint](legacy-endpoint/README.md) | CWE-489 | API9:2023 | handler-unit |
| [Unsafe upstream data](unsafe-upstream-data/README.md) | CWE-20 | API10:2023 | handler-unit |
| [SQL injection](sql-injection/README.md) | CWE-89 | A05:2025 | handler-unit |
