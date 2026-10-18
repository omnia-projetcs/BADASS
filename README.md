# BADASS

**Broken Application Designed for Auditing Security Scanners**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![Benchmark Cases](https://img.shields.io/badge/Cases-287%20pairs-brightgreen.svg)](catalog/cases.json)
[![Technologies](https://img.shields.io/badge/Technologies-14%20stacks-informational.svg)](docs/TECHNOLOGY-MATRIX.md)
[![CWE Weaknesses](https://img.shields.io/badge/CWE-55%20weaknesses-orange.svg)](docs/CWE-MATRIX.md)
[![OWASP Coverage](https://img.shields.io/badge/OWASP-30%20categories-red.svg)](docs/OWASP-MATRIX.md)
[![Benchmark Methodology](https://img.shields.io/badge/Benchmark-Methodology-blueviolet.svg)](docs/BENCHMARK.md)

> **GitHub Topics & Tags:** `security-benchmark` · `vulnerability-detection` · `sast` · `dast` · `cwe` · `owasp` · `appsec` · `security-scanner` · `code-auditing` · `static-analysis` · `security-testing` · `docker`

An executable security benchmark for validating vulnerability detection and remediation across languages,
REST APIs, CGI handlers and AI-assisted audit workflows. Each case includes deliberately vulnerable
code, a corrected counterpart, benign inputs, attack inputs and machine-readable expectations.
Functional and robustness vectors also check useful operations and malformed input.

**287 case pairs · 14 technology sections · 55 distinct CWE weaknesses · 30 OWASP categories represented**

This is a local laboratory containing intentional vulnerabilities. Use synthetic data and the isolated
container workflow. No service is exposed publicly, and no real credentials or external model calls are required.

## Quick start

```sh
# Validate metadata and run the Python section with the installed runtime.
python3 tools/lab.py validate
python3 tools/lab.py test --language python --strict

# Run the mandatory nonempty smoke gate.
make smoke

# Build all runtimes, then run every case with external networking disabled.
make container-build
make container-test
```

Python 3.11+ is sufficient for the tooling, Python, CGI, REST API and AI boundary sections.
The full Linux suite uses GCC/G++, Go, PHP 8+, Node.js, TypeScript, .NET 8 SDK, JDK 17+, Ruby and Rust.
Docker installs these runtimes without changing your host installation. The first image build needs network access.
The container regression report is written to `reports/container-regression.json`.

**SQL injection (CWE-89) is implemented in every technology section**, using actual SQLite queries
and parameter-bound corrections. The image includes the required language drivers.
Run all SQL injection cases with:

```sh
make container-test LAB_ARGS='test --cwe CWE-89 --strict --output reports/sql-injection.json'
```

See [SQL injection cases, drivers and test coverage](docs/SQL-INJECTION.md).

## Vulnerable dependencies

Two executable Node.js cases cover **CWE-1395**: a [direct dependency](labs/node/vulnerable-dependency/README.md)
and a [transitive dependency](labs/node/vulnerable-transitive-dependency/README.md).
Both use real pinned `lodash.merge` releases, package manifests and integrity-checked lockfiles.
The correction upgrades the dependency while retaining the same application code.

```sh
make dependency-prepare  # Install pinned packages; needs npm registry access on a cold cache.
make dependency-test     # 24 variant/vector checks; no network required.
```

Prepare these packages before running the Node.js section with the general runner.
See [dependency fixtures, advisory and SCA evaluation](docs/DEPENDENCIES.md).

## Exploit-DB inspired cases

Five original Python fixtures model weaknesses documented in public Exploit-DB entries:

- [SQL login bypass](labs/python/sql-login-bypass/README.md) (EDB-41029).
- [ZIP extraction traversal](labs/python/zip-slip/README.md) (EDB-39816).
- [Password-reset Host poisoning](labs/python/password-reset-host/README.md) (EDB-52485).
- [Unrestricted upload](labs/python/unrestricted-upload/README.md) (EDB-45169).
- [XML external entity file disclosure](labs/python/xxe/README.md) (EDB-43113).

Each includes a corrected counterpart, synthetic inputs and regression expectations.
These are teaching models, not reproductions of the affected products. Source references
and scope limits appear in each case README.

## Coverage by technology

The shared baseline targets **16 weakness families in all 14 sections**.
C and C++ also have explicit native memory, format-string and integer-arithmetic targets.
Counts below come from exact CWE mappings. They describe source pairs and regression vectors;
execution results remain in the regression reports.

| Technology | Case pairs | Distinct CWE | Shared baseline | Planned targets |
|---|---:|---:|---:|---:|
| [C](labs/c/README.md) | 24 | 24 | 16/16 | 24/24 |
| [C++](labs/cpp/README.md) | 24 | 24 | 16/16 | 24/24 |
| [Go](labs/go/README.md) | 16 | 16 | 16/16 | 16/16 |
| [PHP](labs/php/README.md) | 16 | 16 | 16/16 | 16/16 |
| [REST API (Python handlers)](labs/rest-api/README.md) | 28 | 27 | 16/16 | 16/16 |
| [Node.js](labs/node/README.md) | 19 | 18 | 16/16 | 16/16 |
| [Python](labs/python/README.md) | 36 | 31 | 16/16 | 16/16 |
| [CGI (Python)](labs/cgi/README.md) | 16 | 16 | 16/16 | 16/16 |
| [.NET / C#](labs/dotnet/README.md) | 16 | 16 | 16/16 | 16/16 |
| [TypeScript](labs/typescript/README.md) | 17 | 17 | 16/16 | 16/16 |
| [Java](labs/java/README.md) | 17 | 17 | 16/16 | 16/16 |
| [Ruby](labs/ruby/README.md) | 16 | 16 | 16/16 | 16/16 |
| [Rust](labs/rust/README.md) | 17 | 17 | 16/16 | 16/16 |
| [AI / LLM boundaries](labs/ai/README.md) | 25 | 23 | 16/16 | 16/16 |

See the [baseline and native targets](docs/CORE-MATRIX.md) and the
[complete CWE × technology matrix](docs/TECHNOLOGY-MATRIX.md).
The latter includes every weakness in the pinned taxonomy. Missing cases outside the declared
targets remain `unassessed`; this does not mean they are impossible in that language.

## Vulnerabilities by technology

Every vulnerability currently implemented is listed below. Links open the case documentation, including
the vulnerable and corrected source files. A case in the table is not a claim of full CWE coverage.

| Technology | Cases | Implemented vulnerabilities (CWE) |
|---|---:|---|
| [C](labs/c/README.md) | 24 | [Cross-site scripting (XSS)](labs/c/xss/README.md) (CWE-79)<br>[Path traversal](labs/c/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/c/command-injection/README.md) (CWE-78)<br>[Stack buffer overflow](labs/c/stack-buffer-overflow/README.md) (CWE-121)<br>[Format string](labs/c/format-string/README.md) (CWE-134)<br>[SQL injection](labs/c/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/c/idor/README.md) (CWE-639)<br>[Missing authorization](labs/c/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/c/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/c/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/c/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/c/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/c/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/c/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/c/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/c/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/c/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/c/symlink-following/README.md) (CWE-59)<br>[Heap buffer overflow](labs/c/heap-buffer-overflow/README.md) (CWE-122)<br>[Use after free](labs/c/use-after-free/README.md) (CWE-416)<br>[Double free](labs/c/double-free/README.md) (CWE-415)<br>[Null dereference](labs/c/null-dereference/README.md) (CWE-476)<br>[Out of bounds read](labs/c/out-of-bounds-read/README.md) (CWE-125)<br>[Integer overflow](labs/c/integer-overflow/README.md) (CWE-190) |
| [C++](labs/cpp/README.md) | 24 | [Cross-site scripting (XSS)](labs/cpp/xss/README.md) (CWE-79)<br>[Path traversal](labs/cpp/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/cpp/command-injection/README.md) (CWE-78)<br>[Out of bounds read](labs/cpp/out-of-bounds-read/README.md) (CWE-125)<br>[SQL injection](labs/cpp/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/cpp/idor/README.md) (CWE-639)<br>[Missing authorization](labs/cpp/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/cpp/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/cpp/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/cpp/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/cpp/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/cpp/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/cpp/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/cpp/business-logic/README.md) (CWE-1284)<br>[HTTP response header injection](labs/cpp/header-injection/README.md) (CWE-113)<br>[World readable secret](labs/cpp/world-readable-secret/README.md) (CWE-732)<br>[Symlink following](labs/cpp/symlink-following/README.md) (CWE-59)<br>[Heap buffer overflow](labs/cpp/heap-buffer-overflow/README.md) (CWE-122)<br>[Use after free](labs/cpp/use-after-free/README.md) (CWE-416)<br>[Double free](labs/cpp/double-free/README.md) (CWE-415)<br>[Null dereference](labs/cpp/null-dereference/README.md) (CWE-476)<br>[Stack buffer overflow](labs/cpp/stack-buffer-overflow/README.md) (CWE-121)<br>[Format string](labs/cpp/format-string/README.md) (CWE-134)<br>[Integer overflow](labs/cpp/integer-overflow/README.md) (CWE-190) |
| [Go](labs/go/README.md) | 16 | [Cross-site scripting (XSS)](labs/go/xss/README.md) (CWE-79)<br>[Path traversal](labs/go/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/go/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/go/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/go/idor/README.md) (CWE-639)<br>[Missing authorization](labs/go/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/go/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/go/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/go/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/go/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/go/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/go/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/go/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/go/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/go/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/go/symlink-following/README.md) (CWE-59) |
| [PHP](labs/php/README.md) | 16 | [Cross-site scripting (XSS)](labs/php/xss/README.md) (CWE-79)<br>[Path traversal](labs/php/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/php/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/php/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/php/idor/README.md) (CWE-639)<br>[Missing authorization](labs/php/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/php/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/php/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/php/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/php/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/php/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/php/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/php/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/php/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/php/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/php/symlink-following/README.md) (CWE-59) |
| [REST API (Python handlers)](labs/rest-api/README.md) | 28 | [Broken object-level authorization (BOLA)](labs/rest-api/bola/README.md) (CWE-639)<br>[Broken authentication](labs/rest-api/broken-authentication/README.md) (CWE-287)<br>[Property authorization](labs/rest-api/property-authorization/README.md) (CWE-915)<br>[Resource consumption](labs/rest-api/resource-consumption/README.md) (CWE-770)<br>[Function authorization](labs/rest-api/function-authorization/README.md) (CWE-862)<br>[Business flow abuse](labs/rest-api/business-flow-abuse/README.md) (CWE-799)<br>[Server-side request forgery (SSRF)](labs/rest-api/ssrf/README.md) (CWE-918)<br>[Credentialed CORS misconfiguration](labs/rest-api/cors-misconfiguration/README.md) (CWE-942)<br>[Legacy endpoint](labs/rest-api/legacy-endpoint/README.md) (CWE-489)<br>[Unsafe upstream data](labs/rest-api/unsafe-upstream-data/README.md) (CWE-20)<br>[SQL injection](labs/rest-api/sql-injection/README.md) (CWE-89)<br>[Hardcoded credentials](labs/rest-api/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/rest-api/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/rest-api/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/rest-api/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/rest-api/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/rest-api/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/rest-api/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/rest-api/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/rest-api/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/rest-api/symlink-following/README.md) (CWE-59)<br>[Cross-site scripting (XSS)](labs/rest-api/xss/README.md) (CWE-79)<br>[Path traversal](labs/rest-api/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/rest-api/command-injection/README.md) (CWE-78)<br>[Multi tenant authorization](labs/rest-api/multi-tenant-authorization/README.md) (CWE-863)<br>[Order workflow](labs/rest-api/order-workflow/README.md) (CWE-841)<br>[SSRF through an HTTP redirect](labs/rest-api/ssrf-redirect/README.md) (CWE-918)<br>[Concurrent duplicate shipment](labs/rest-api/order-concurrency/README.md) (CWE-362) |
| [Node.js](labs/node/README.md) | 19 | [Cross-site scripting (XSS)](labs/node/xss/README.md) (CWE-79)<br>[Path traversal](labs/node/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/node/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/node/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/node/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/node/idor/README.md) (CWE-639)<br>[Missing authorization](labs/node/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/node/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/node/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/node/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/node/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/node/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/node/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/node/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/node/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/node/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/node/symlink-following/README.md) (CWE-59)<br>[Vulnerable dependency](labs/node/vulnerable-dependency/README.md) (CWE-1395)<br>[Vulnerable transitive dependency](labs/node/vulnerable-transitive-dependency/README.md) (CWE-1395) |
| [Python](labs/python/README.md) | 36 | [Cross-site scripting (XSS)](labs/python/xss/README.md) (CWE-79)<br>[Path traversal](labs/python/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/python/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/python/sql-injection/README.md) (CWE-89)<br>[Code injection](labs/python/code-injection/README.md) (CWE-95)<br>[Unsafe deserialization](labs/python/unsafe-deserialization/README.md) (CWE-502)<br>[Insecure direct object reference (IDOR)](labs/python/idor/README.md) (CWE-639)<br>[Mass assignment](labs/python/mass-assignment/README.md) (CWE-915)<br>[Cross-site request forgery (CSRF)](labs/python/csrf/README.md) (CWE-352)<br>[Session fixation](labs/python/session-fixation/README.md) (CWE-384)<br>[Weak password hash](labs/python/weak-password-hash/README.md) (CWE-916)<br>[Hardcoded credentials](labs/python/hardcoded-credentials/README.md) (CWE-798)<br>[Predictable token](labs/python/predictable-token/README.md) (CWE-330)<br>[Log injection](labs/python/log-injection/README.md) (CWE-117)<br>[Sensitive logging](labs/python/sensitive-logging/README.md) (CWE-532)<br>[Error disclosure](labs/python/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/python/fail-open/README.md) (CWE-636)<br>[Unverified update](labs/python/unverified-update/README.md) (CWE-494)<br>[Untrusted plugin](labs/python/untrusted-plugin/README.md) (CWE-829)<br>[Open redirect](labs/python/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/python/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/python/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/python/world-readable-secret/README.md) (CWE-732)<br>[Disabled TLS verification](labs/python/tls-verification/README.md) (CWE-295)<br>[Missing security audit events](labs/python/missing-audit/README.md) (CWE-778)<br>[Missing authorization](labs/python/missing-authorization/README.md) (CWE-862)<br>[HTTP response header injection](labs/python/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/python/symlink-following/README.md) (CWE-59)<br>[SQL injection in an ORDER BY identifier](labs/python/sql-order-by/README.md) (CWE-89)<br>[Second-order SQL injection](labs/python/sql-second-order/README.md) (CWE-89)<br>[XSS in an HTML attribute](labs/python/xss-attribute/README.md) (CWE-79)<br>[Sql login bypass](labs/python/sql-login-bypass/README.md) (CWE-89)<br>[Zip slip](labs/python/zip-slip/README.md) (CWE-22)<br>[Password reset host](labs/python/password-reset-host/README.md) (CWE-346)<br>[Unrestricted upload](labs/python/unrestricted-upload/README.md) (CWE-434)<br>[XML external entities (XXE)](labs/python/xxe/README.md) (CWE-611) |
| [CGI (Python)](labs/cgi/README.md) | 16 | [Cross-site scripting (XSS)](labs/cgi/xss/README.md) (CWE-79)<br>[HTTP response header injection](labs/cgi/header-injection/README.md) (CWE-113)<br>[SQL injection](labs/cgi/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/cgi/idor/README.md) (CWE-639)<br>[Missing authorization](labs/cgi/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/cgi/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/cgi/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/cgi/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/cgi/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/cgi/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/cgi/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/cgi/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/cgi/world-readable-secret/README.md) (CWE-732)<br>[Symlink following](labs/cgi/symlink-following/README.md) (CWE-59)<br>[Path traversal](labs/cgi/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/cgi/command-injection/README.md) (CWE-78) |
| [.NET / C#](labs/dotnet/README.md) | 16 | [Cross-site scripting (XSS)](labs/dotnet/xss/README.md) (CWE-79)<br>[Path traversal](labs/dotnet/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/dotnet/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/dotnet/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/dotnet/idor/README.md) (CWE-639)<br>[Missing authorization](labs/dotnet/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/dotnet/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/dotnet/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/dotnet/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/dotnet/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/dotnet/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/dotnet/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/dotnet/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/dotnet/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/dotnet/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/dotnet/symlink-following/README.md) (CWE-59) |
| [TypeScript](labs/typescript/README.md) | 17 | [Cross-site scripting (XSS)](labs/typescript/xss/README.md) (CWE-79)<br>[Path traversal](labs/typescript/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/typescript/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/typescript/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/typescript/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/typescript/idor/README.md) (CWE-639)<br>[Missing authorization](labs/typescript/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/typescript/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/typescript/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/typescript/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/typescript/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/typescript/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/typescript/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/typescript/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/typescript/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/typescript/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/typescript/symlink-following/README.md) (CWE-59) |
| [Java](labs/java/README.md) | 17 | [Cross-site scripting (XSS)](labs/java/xss/README.md) (CWE-79)<br>[Path traversal](labs/java/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/java/command-injection/README.md) (CWE-78)<br>[XML external entities (XXE)](labs/java/xxe/README.md) (CWE-611)<br>[SQL injection](labs/java/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/java/idor/README.md) (CWE-639)<br>[Missing authorization](labs/java/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/java/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/java/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/java/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/java/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/java/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/java/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/java/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/java/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/java/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/java/symlink-following/README.md) (CWE-59) |
| [Ruby](labs/ruby/README.md) | 16 | [Cross-site scripting (XSS)](labs/ruby/xss/README.md) (CWE-79)<br>[Path traversal](labs/ruby/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/ruby/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/ruby/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/ruby/idor/README.md) (CWE-639)<br>[Missing authorization](labs/ruby/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/ruby/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/ruby/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/ruby/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/ruby/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/ruby/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/ruby/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/ruby/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/ruby/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/ruby/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/ruby/symlink-following/README.md) (CWE-59) |
| [Rust](labs/rust/README.md) | 17 | [Cross-site scripting (XSS)](labs/rust/xss/README.md) (CWE-79)<br>[Path traversal](labs/rust/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/rust/command-injection/README.md) (CWE-78)<br>[Integer overflow](labs/rust/integer-overflow/README.md) (CWE-190)<br>[SQL injection](labs/rust/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/rust/idor/README.md) (CWE-639)<br>[Missing authorization](labs/rust/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/rust/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/rust/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/rust/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/rust/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/rust/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/rust/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/rust/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/rust/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/rust/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/rust/symlink-following/README.md) (CWE-59) |
| [AI / LLM boundaries](labs/ai/README.md) | 25 | [Prompt trust boundary](labs/ai/prompt-trust-boundary/README.md) (CWE-1427)<br>[Sensitive context](labs/ai/sensitive-context/README.md) (CWE-200)<br>[Model artifact integrity](labs/ai/model-artifact-integrity/README.md) (CWE-494)<br>[Training data poisoning](labs/ai/training-data-poisoning/README.md) (CWE-20)<br>[Unsafe model output](labs/ai/unsafe-model-output/README.md) (CWE-79)<br>[Excessive agency](labs/ai/excessive-agency/README.md) (CWE-862)<br>[System prompt leakage](labs/ai/system-prompt-leakage/README.md) (CWE-200)<br>[Cross tenant retrieval](labs/ai/cross-tenant-retrieval/README.md) (CWE-863)<br>[Unverified security claim](labs/ai/unverified-security-claim/README.md) (CWE-345)<br>[Unbounded agent loop](labs/ai/unbounded-agent-loop/README.md) (CWE-834)<br>[SQL injection](labs/ai/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/ai/idor/README.md) (CWE-639)<br>[Hardcoded credentials](labs/ai/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/ai/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/ai/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/ai/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/ai/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/ai/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/ai/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/ai/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/ai/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/ai/symlink-following/README.md) (CWE-59)<br>[Path traversal](labs/ai/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/ai/command-injection/README.md) (CWE-78)<br>[Tool argument scope](labs/ai/tool-argument-scope/README.md) (CWE-863) |

## What coverage means

The [complete CWE matrix](docs/CWE-MATRIX.md) enumerates all **1450 entries** from MITRE CWE
**4.20**: **969 weaknesses** plus categories and views. **55 weaknesses** currently
have direct executable cases; **914 remain explicit gaps**. Categories and views are marked
`taxonomy-only`. The matrix is exhaustive for this snapshot; the executable corpus is not.

The [OWASP matrix](docs/OWASP-MATRIX.md) tracks all categories in **Web Top 10:2025**,
**API Security Top 10:2023**, and **LLM Top 10:2025**. Each has at least one mapped example.
These are pinned editions, not a claim to cover every OWASP project or every scenario within a category.
ASVS, WSTG, mobile, hardware and other domains still require additional work.

Most language cases are small executable source slices. API cases mainly exercise handler boundaries;
the SSRF case includes a real loopback HTTP request. AI boundary tests run application controls, not a model.
See [benchmark methodology and assumptions](docs/BENCHMARK.md).

## Run, score and repair

```sh
python3 tools/lab.py list --language java
python3 tools/lab.py test --case java/xxe --strict
python3 tools/lab.py test --cwe CWE-89 --strict --output reports/sql-injection.json
python3 tools/lab.py test --strict --output reports/regression.json
python3 tools/lab.py coverage --output reports/coverage.json
python3 tools/lab.py score --findings findings.json --output reports/score.json
python3 -m unittest discover -s tests -v
```

The runner checks both variants against the same vectors. A missing runtime is reported as `skip`;
`--strict` turns skips into failures. Failed builds, timeouts and unrelated crashes never count as successful tests.
C/C++ memory cases use AddressSanitizer and UndefinedBehaviorSanitizer.

The scorer accepts normalized findings with `case_id`, `variant`, and `cwe`. It reports precision, recall,
false positives and false negatives, deduplicating repeated findings. See the [input format](docs/BENCHMARK.md#detection-scoring).
Evaluate a candidate correction in the `fixed/` source while keeping test expectations trusted and unchanged.

File expectations inspect real contents, file types and permissions after execution. Trusted oracles
exercise password, reset-token and session operations without accepting a candidate self-assessment.
An empty selection or an entirely skipped execution cannot pass. See the
[correction notes](docs/REVIEW-CHANGES.md) and [French application guide](GUIDE_CORRECTIONS_FR.md).

For a scanner corpus without case/variant directory labels, keep the mapping outside the exported directory:

```sh
python3 tools/export_blind.py --output ../badass-blind --mapping ../badass-blind-map.json
```

The exporter preserves source bytes. It removes directory labels and documentation, not all possible
semantic clues in code; it does not establish that a scanner or model has never seen the sources.

## AI prompt injection, reverse repair injection and jailbreaks

Ten [inert attack payloads](catalog/ai-attacks.json) cover direct overrides, authority spoofing, roleplay,
encoded jailbreaks, source comments, retrieval content, tool responses, synthetic canary requests,
unauthorized tool escalation and instructions to introduce vulnerabilities during a repair.

The [AI evaluation protocol](docs/AI-TESTING.md) explains how to collect independent observations and score
finding suppression, disclosure, unauthorized actions and repair regressions:

```sh
python3 tools/ai_evaluate.py observations.json --output reports/ai-evaluation.json
```

No real-model resilience result is claimed. Missing observations remain untested. Application boundary
tests do not prove that an LLM resists prompt injection or jailbreaks.

## Repository layout

```text
catalog/       Case contracts, CWE snapshot, OWASP references and AI attack manifest
labs/          One section per technology; vulnerable/ and fixed/ source pairs
tools/         Regression runner, scorer, CWE importer and documentation renderer
tests/         Regression tests for the benchmark tooling itself
docs/          Complete CWE matrix, OWASP mappings and evaluation protocols
reports/       Generated execution and scoring reports (ignored by Git)
```

## Add a case or update the catalog

1. Add a focused source pair under `labs/<technology>/<case>/{vulnerable,fixed}/`.
2. Add an entry to `catalog/cases.json` with its CWE, OWASP mappings, scope, remediation and test vectors.
3. Include at least one benign vector and one attack vector with different vulnerable/fixed outcomes.
4. Run catalog validation, the affected regression, tooling tests and `python3 tools/render_docs.py`.
5. Keep limitations explicit; do not label unimplemented weaknesses as covered.

To refresh the CWE snapshot, download an official XML ZIP from [MITRE](https://cwe.mitre.org/data/downloads.html),
then run `python3 tools/import_cwe.py /path/to/cwec_VERSION.xml.zip` and regenerate the documentation.
Review mappings, metadata and third-party notices when changing reference versions.

## References and license

- [MITRE CWE downloads](https://cwe.mitre.org/data/downloads.html)
- [OWASP Web Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/)
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/)
- [OWASP LLM Top 10:2025](https://genai.owasp.org/llm-top-10/)

Project code: [MIT License](LICENSE). Taxonomy data and reference attribution:
[third-party notices](THIRD_PARTY_NOTICES.md). No MITRE or OWASP endorsement is implied.
