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
| [Cross-site scripting (XSS)](xss/README.md) | CWE-79 | A05:2025 | handler-unit |
| [Path traversal](path-traversal/README.md) | CWE-22 | A01:2025 | executable |
| [Command injection](command-injection/README.md) | CWE-78 | A05:2025 | executable |
| [Multi tenant authorization](multi-tenant-authorization/README.md) | CWE-863 | A01:2025, API1:2023 | handler-unit |
| [Order workflow](order-workflow/README.md) | CWE-841 | A06:2025, API6:2023 | state-machine-unit |
| [SSRF through an HTTP redirect](ssrf-redirect/README.md) | CWE-918 | API7:2023 | loopback-integration |
| [Concurrent duplicate shipment](order-concurrency/README.md) | CWE-362 | A06:2025, API6:2023 | transaction-concurrency-unit |
| [Tenant cache](tenant-cache/README.md) | CWE-488 | A01:2025, API1:2023 | executable |
| [Tenant admin scope](tenant-admin-scope/README.md) | CWE-863 | A01:2025, API5:2023 | executable |
| [Tenant export worker](tenant-export-worker/README.md) | CWE-863 | A01:2025, API1:2023 | executable |
| [Tenant bulk update](tenant-bulk-update/README.md) | CWE-863 | A01:2025, API1:2023 | executable |
| [Tenant signed download](tenant-signed-download/README.md) | CWE-863 | A01:2025, API1:2023 | executable |
| [Tenant session switch](tenant-session-switch/README.md) | CWE-863 | A01:2025, API5:2023 | executable |
| [Tenant storage prefix](tenant-storage-prefix/README.md) | CWE-22 | A01:2025, API1:2023 | executable |
| [Coupon stacking](coupon-stacking/README.md) | CWE-841 | API6:2023, A06:2025 | state-machine-unit |
| [Currency arbitrage](currency-arbitrage/README.md) | CWE-841, CWE-682 | API6:2023, A06:2025 | handler-unit |
| [Split order quota](split-order-quota/README.md) | CWE-799, CWE-841 | API6:2023, A06:2025 | state-machine-unit |
| [NoSQL operator injection](nosql-injection/README.md) | CWE-943 | A05:2025, API8:2023 | handler-unit |
| [GraphQL depth amplification and introspection](graphql-depth-amplification/README.md) | CWE-400, CWE-200 | API4:2023, A06:2025 | handler-unit |
| [User enumeration](user-enumeration/README.md) | CWE-203, CWE-208 | A07:2025, API2:2023 | handler-unit |
| [Web cache poisoning](web-cache-poisoning/README.md) | CWE-525, CWE-444 | A02:2025, API8:2023 | handler-unit |
