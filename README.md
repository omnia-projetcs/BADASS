# BADASS

**Broken Application Designed for Auditing Security Scanners**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)
[![Benchmark Cases](https://img.shields.io/badge/Cases-395%20pairs-brightgreen.svg)](catalog/cases.json)
[![Technologies](https://img.shields.io/badge/Technologies-14%20stacks-informational.svg)](docs/TECHNOLOGY-MATRIX.md)
[![CWE Weaknesses](https://img.shields.io/badge/CWE-102%20weaknesses-orange.svg)](docs/CWE-MATRIX.md)
[![OWASP Coverage](https://img.shields.io/badge/OWASP-30%20categories-red.svg)](docs/OWASP-MATRIX.md)
[![Benchmark Methodology](https://img.shields.io/badge/Benchmark-Methodology-blueviolet.svg)](docs/BENCHMARK.md)

> **GitHub Topics & Tags:** `security-benchmark` · `vulnerability-detection` · `sast` · `dast` · `cwe` · `owasp` · `appsec` · `security-scanner` · `code-auditing` · `static-analysis` · `security-testing` · `docker`

An executable security benchmark for validating vulnerability detection and remediation across languages,
REST APIs, CGI handlers and AI-assisted audit workflows. Each case includes deliberately vulnerable
code, a corrected counterpart, benign inputs, attack inputs and machine-readable expectations.
Functional and robustness vectors also check useful operations and malformed input.

**395 case pairs · 14 technology sections · 102 distinct CWE weaknesses · 30 OWASP categories represented**

This is a local laboratory containing intentional vulnerabilities. Use synthetic data and the isolated
container workflow. No service is exposed publicly, and no real credentials or external model calls are required.

## Catalog statistics

| Metric | Count |
|---|---:|
| Case pairs | 395 |
| Vulnerable and corrected variants | 790 |
| Distinct CWE weaknesses | 102 |
| Technology sections | 14 |
| Regression vectors | 1999 |
| Declared variant/vector checks | 3998 |

Each vector has expectations for both variants. These are catalog counts, not passed-test totals;
execution evidence is recorded separately in regression reports.

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

## Micro-server (Docker multi-protocol network targets)

All 14 technology stacks (790 vulnerable/fixed targets) plus non-HTTP LAN protocol listeners can be
served inside an unprivileged, read-only Docker container, so you can test scanners or clients from
the network only.

```sh
./run.sh               # build (first run) and start on 127.0.0.1 (HTTP :8808 + protocol ports)
./run.sh --blind       # opaque ids; private answer key copied to .netlab/mapping.json
./run.sh logs          # follow container logs
./run.sh status        # show container status
./run.sh stop          # stop and remove the container
./update.sh            # git pull --ff-only, rebuild images, restart if running
./uninstall.sh         # stop container, remove images and generated files (--purge deletes checkout)
```

Services published by default (`GET /` opens a live status dashboard of active/inactive services, stacks, and targets; `GET /status.json` and `GET /services.json` expose the machine-readable view):
- **HTTP** `:8808` and **HTTPS (TLS)** `:8443` — all 790 catalog targets (`/t/<language>/<case>/<variant>` and `/targets.json`).
- **FTP** `:2121` (data `:2122`) — anonymous / default password login (`CWE-798`), path traversal via `RETR` (`CWE-22`).
- **Telnet / CLI** `:2323` — default password (`CWE-798`), command injection (`CWE-78`), `@file` expansion (`CWE-73`), error disclosure (`CWE-209`).
- **SMTP** `:2525` — `VRFY` enumeration, header/log injection (`CWE-113`/`CWE-117`), unverified reset recipients (`CWE-640`).
- **LDAPv3** `:3389` — real ASN.1/BER search filter injection (`CWE-90`).
- **DNS** `:5353/udp+tcp` — DNS rebinding on `rebind.badass.local` (`CWE-918`) and `TXT` disclosure on `secret.badass.local`.
- **RESP (Redis-like)** `:6379` — unauthenticated `INFO` disclosure (`CWE-209`) and `EVAL` code injection (`CWE-95`).
- **Raw TCP** `:9001` — line protocol (`LIST`, `RUN <target_id> <input>`) to invoke any target over TCP.

Options: `PORT=9000 ./run.sh` changes the HTTP port, `BIND=0.0.0.0 ./run.sh` exposes services on an
**isolated** lab LAN, and extra flags are passed to `tools/netserve.py` (`--language`, `--cwe`,
`--proto-variant fixed`). All ports bind to `127.0.0.1` by default; never expose them on an
untrusted network.

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

26 original Python fixtures model weaknesses documented in public Exploit-DB entries:

- [Sql login bypass](labs/python/sql-login-bypass/README.md) (EDB-41029).
- [Zip slip](labs/python/zip-slip/README.md) (EDB-39816).
- [Password reset host](labs/python/password-reset-host/README.md) (EDB-52485).
- [Unrestricted upload](labs/python/unrestricted-upload/README.md) (EDB-45169).
- [XML external entities (XXE)](labs/python/xxe/README.md) (EDB-43113).
- [Jwt default key](labs/python/jwt-default-key/README.md) (EDB-51354).
- [Jwt disabled user](labs/python/jwt-disabled-user/README.md) (EDB-51992).
- [Csv formula injection](labs/python/csv-formula-injection/README.md) (EDB-49805).
- [Argument injection](labs/python/argument-injection/README.md) (EDB-44993).
- [File create race](labs/python/file-create-race/README.md) (EDB-24749).
- [Double-decoding path traversal](labs/python/double-decoding-traversal/README.md) (EDB-50406).
- [Item-name template injection](labs/python/item-template-injection/README.md) (EDB-52030).
- [CGI redirect response splitting](labs/python/cgi-redirect-splitting/README.md) (EDB-49923).
- [DNS rebinding SSRF](labs/python/dns-rebinding-ssrf/README.md) (EDB-52651).
- [SVG resource SSRF](labs/python/svg-resource-ssrf/README.md) (EDB-52551).
- [Remote-file import SSRF](labs/python/remote-import-ssrf/README.md) (EDB-51030).
- [TAR symlink escape](labs/python/tar-symlink-escape/README.md) (EDB-43002).
- [Factory authentication bypass](labs/python/factory-auth-bypass/README.md) (EDB-40156).
- [Query-clause authorization bypass](labs/python/query-clause-authorization/README.md) (EDB-44068).
- [Backslash open redirect](labs/python/backslash-open-redirect/README.md) (EDB-43592).
- [Log4Shell: message lookup injection](labs/python/log4shell-lookup/README.md) (EDB-51183).
- [TeamCity: dispatch authentication bypass](labs/python/teamcity-dispatch-bypass/README.md) (EDB-52411).
- [Confluence: pre-auth expression evaluation](labs/python/confluence-expression-dispatch/README.md) (EDB-50952).
- [FortiOS: forwarded-header authentication bypass](labs/python/fortios-forwarded-auth/README.md) (EDB-51092).
- [Confluence: setup-state binding](labs/python/confluence-setup-reopen/README.md) (EDB-51829).
- [ImageTragick: delegate shell injection](labs/python/imagetragick-delegate/README.md) (EDB-39767).

Each includes a corrected counterpart, synthetic inputs and regression expectations.
These are teaching models, not reproductions of the affected products. Source references
and scope limits appear in each case README.

## Named CVE teaching models

17 focused cases model documented CVE mechanisms across runtimes, APIs, parsers and services.
The PHP2Shell family has separate cases for its two CVEs. These original reduced models
demonstrate specific failure mechanisms; they do not reproduce product-level RCE.

| Case | CVE | Implementation scope |
|---|---|---|
| [PHP2Shell: request OOM cleanup](labs/c/php2shell-oom/README.md) | CVE-2026-109618 | native-model |
| [PHP2Shell: stale worker state](labs/c/php2shell-stale-state/README.md) | CVE-2026-109619 | native-model |
| [Node2Shell: Brotli block-switch status](labs/c/node2shell-block-switch/README.md) | CVE-2026-111497 | native-model |
| [PHP-CGI best-fit argument injection](labs/c/php-cgi-best-fit/README.md) | CVE-2024-4577 | native-model |
| [Log4Shell: message lookup injection](labs/python/log4shell-lookup/README.md) | CVE-2021-44228 | handler-model |
| [TeamCity: dispatch authentication bypass](labs/python/teamcity-dispatch-bypass/README.md) | CVE-2024-27198 | handler-model |
| [Confluence: pre-auth expression evaluation](labs/python/confluence-expression-dispatch/README.md) | CVE-2022-26134 | handler-model |
| [Spring4Shell: class-loader property binding](labs/python/spring4shell-binding/README.md) | CVE-2022-22965 | handler-model |
| [Jenkins CLI: pre-auth file expansion](labs/python/jenkins-cli-atfile/README.md) | CVE-2024-23897 | executable |
| [FortiOS: forwarded-header authentication bypass](labs/python/fortios-forwarded-auth/README.md) | CVE-2022-40684 | handler-model |
| [Confluence: setup-state binding](labs/python/confluence-setup-reopen/README.md) | CVE-2023-22515 | handler-model |
| [GitLab: unverified reset recipients](labs/python/gitlab-reset-recipients/README.md) | CVE-2023-7028 | handler-model |
| [MinIO: bootstrap credential disclosure](labs/python/minio-bootstrap-disclosure/README.md) | CVE-2023-28432 | handler-model |
| [ActiveMQ: unchecked throwable construction](labs/python/activemq-openwire-type/README.md) | CVE-2023-46604 | handler-model |
| [Zabbix: role projection SQL injection](labs/python/zabbix-role-projection/README.md) | CVE-2024-42327 | executable |
| [ImageTragick: delegate shell injection](labs/python/imagetragick-delegate/README.md) | CVE-2016-3714 | executable |
| [Apache HTTP Server: proxy request splitting](labs/python/apache-proxy-request-splitting/README.md) | CVE-2023-25690 | executable |

Memory-safety cases execute under AddressSanitizer and exercise actual freed-memory reads or
buffer writes. Python cases inspect real logs, response headers and SQLite state, with
offline lookup dependencies. See [scope, upstream advisories and regression commands](docs/NAMED-CVES.md).

## General security boundaries

These Python and Node.js examples include vulnerable and corrected implementations, executable vectors
and tests that inspect actual process results, file contents or committed database state.
They use standard libraries and synthetic local data.

| Case | CWE | Observable effect |
|---|---|---|
| [Argument injection](labs/python/argument-injection/README.md) | CWE-88 | User data becomes a child-process option. |
| [Format-string disclosure](labs/python/format-string-disclosure/README.md) | CWE-134 | Object traversal exposes private data. |
| [File creation race](labs/python/file-create-race/README.md) | CWE-367 | A substituted symlink redirects a file write. |
| [JSON parser conflict](labs/python/json-parser-conflict/README.md) | CWE-436 | Duplicate keys change the amount actually debited. |
| [Unicode path validation](labs/python/unicode-path-validation/README.md) | CWE-180 | Normalization introduces traversal after validation. |
| [Password-reset replay](labs/python/password-reset-replay/README.md) | CWE-640 | A used token changes the password again. |
| [Webhook signature](labs/python/webhook-signature/README.md) | CWE-347 | An unauthenticated event marks an invoice as paid. |
| [Decompression amplification](labs/python/decompression-amplification/README.md) | CWE-409 | Small compressed input exceeds the expanded-data budget. |
| [Session expiration](labs/python/session-expiration/README.md) | CWE-613 | Expired or revoked sessions still retrieve private data. |
| Partial HMAC comparison ([Python](labs/python/partial-signature/README.md), [Node.js](labs/node/partial-signature/README.md)) | CWE-187 | Empty or truncated tags authenticate a message. |
| Client-controlled price ([Python](labs/python/client-price/README.md), [Node.js](labs/node/client-price/README.md)) | CWE-602 | A modified client price creates an underpriced receipt. |
| Permissive origin regex ([Python](labs/python/regex-origin/README.md), [Node.js](labs/node/regex-origin/README.md)) | CWE-625 | Unescaped dots admit unrelated origins to credentialed responses. |
| Signed action replay ([Python](labs/python/signed-action-replay/README.md), [Node.js](labs/node/signed-action-replay/README.md)) | CWE-294 | A captured signed action applies the same debit repeatedly. |

Run the two newest families in both languages and their behavioral tests:

```sh
python3 tools/lab.py test --cwe CWE-625 --strict
python3 tools/lab.py test --cwe CWE-294 --strict
python3 -m unittest discover -s tests -p test_origin_replay_boundaries.py -v
```

These commands require Python 3.11+ and Node.js; the new Node.js cases need no npm packages.

See [general boundary cases, evidence and scope limits](docs/GENERAL-BOUNDARIES.md).

## Tenant isolation

Seven REST API handler cases exercise cross-tenant cache leaks, tenant-scoped roles,
export-worker scope loss, mixed-tenant batch updates, signed download scope,
session switching and storage path boundaries.
Tests inspect real exported files, account snapshots and committed SQLite rows.
See [tenant isolation scenarios and regression commands](docs/TENANT-ISOLATION.md).

## Coverage by technology

The shared baseline targets **16 weakness families in all 14 sections**.
C and C++ also have explicit native memory, format-string and integer-arithmetic targets.
Counts below come from exact CWE mappings. They describe source pairs and regression vectors;
execution results remain in the regression reports.

Both technology tables are generated from [the case catalog](catalog/cases.json).
Regenerate them with `python3 tools/render_docs.py` and check freshness with `--check`.

| Technology | Case pairs | Distinct CWE | Vectors | Declared checks | Shared baseline | Planned targets |
|---|---:|---:|---:|---:|---:|---:|
| [C](labs/c/README.md) | 31 | 31 | 172 | 344 | 16/16 | 24/24 |
| [C++](labs/cpp/README.md) | 27 | 28 | 129 | 258 | 16/16 | 24/24 |
| [Go](labs/go/README.md) | 19 | 19 | 64 | 128 | 16/16 | 16/16 |
| [PHP](labs/php/README.md) | 22 | 22 | 67 | 134 | 16/16 | 16/16 |
| [REST API (Python handlers)](labs/rest-api/README.md) | 42 | 35 | 238 | 476 | 16/16 | 16/16 |
| [Node.js](labs/node/README.md) | 27 | 26 | 151 | 302 | 16/16 | 16/16 |
| [Python](labs/python/README.md) | 83 | 65 | 692 | 1384 | 16/16 | 16/16 |
| [CGI (Python)](labs/cgi/README.md) | 17 | 19 | 60 | 120 | 16/16 | 16/16 |
| [.NET / C#](labs/dotnet/README.md) | 20 | 20 | 66 | 132 | 16/16 | 16/16 |
| [TypeScript](labs/typescript/README.md) | 19 | 19 | 70 | 140 | 16/16 | 16/16 |
| [Java](labs/java/README.md) | 20 | 20 | 63 | 126 | 16/16 | 16/16 |
| [Ruby](labs/ruby/README.md) | 20 | 20 | 63 | 126 | 16/16 | 16/16 |
| [Rust](labs/rust/README.md) | 18 | 19 | 59 | 118 | 16/16 | 16/16 |
| [AI / LLM boundaries](labs/ai/README.md) | 30 | 26 | 105 | 210 | 16/16 | 16/16 |

See the [baseline and native targets](docs/CORE-MATRIX.md) and the
[complete CWE × technology matrix](docs/TECHNOLOGY-MATRIX.md).
The latter includes every weakness in the pinned taxonomy. Missing cases outside the declared
targets remain `unassessed`; this does not mean they are impossible in that language.

## Vulnerabilities by technology

Every vulnerability currently implemented is listed below. Links open the case documentation, including
the vulnerable and corrected source files. A case in the table is not a claim of full CWE coverage.

| Technology | Cases | Implemented vulnerabilities (CWE) |
|---|---:|---|
| [C](labs/c/README.md) | 31 | [Cross-site scripting (XSS)](labs/c/xss/README.md) (CWE-79)<br>[Path traversal](labs/c/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/c/command-injection/README.md) (CWE-78)<br>[Stack buffer overflow](labs/c/stack-buffer-overflow/README.md) (CWE-121)<br>[Format string](labs/c/format-string/README.md) (CWE-134)<br>[SQL injection](labs/c/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/c/idor/README.md) (CWE-639)<br>[Missing authorization](labs/c/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/c/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/c/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/c/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/c/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/c/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/c/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/c/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/c/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/c/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/c/symlink-following/README.md) (CWE-59)<br>[Heap buffer overflow](labs/c/heap-buffer-overflow/README.md) (CWE-122)<br>[Use after free](labs/c/use-after-free/README.md) (CWE-416)<br>[Double free](labs/c/double-free/README.md) (CWE-415)<br>[Null dereference](labs/c/null-dereference/README.md) (CWE-476)<br>[Out of bounds read](labs/c/out-of-bounds-read/README.md) (CWE-125)<br>[Integer overflow](labs/c/integer-overflow/README.md) (CWE-190)<br>[PHP2Shell: request OOM cleanup](labs/c/php2shell-oom/README.md) (CWE-416)<br>[PHP2Shell: stale worker state](labs/c/php2shell-stale-state/README.md) (CWE-416)<br>[Node2Shell: Brotli block-switch status](labs/c/node2shell-block-switch/README.md) (CWE-252, CWE-787)<br>[PHP-CGI best-fit argument injection](labs/c/php-cgi-best-fit/README.md) (CWE-88)<br>[Uninitialized memory](labs/c/uninitialized-memory/README.md) (CWE-457)<br>[Type confusion](labs/c/type-confusion/README.md) (CWE-843)<br>[Signed unsigned conversion](labs/c/signed-unsigned-conversion/README.md) (CWE-195, CWE-681) |
| [C++](labs/cpp/README.md) | 27 | [Cross-site scripting (XSS)](labs/cpp/xss/README.md) (CWE-79)<br>[Path traversal](labs/cpp/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/cpp/command-injection/README.md) (CWE-78)<br>[Out of bounds read](labs/cpp/out-of-bounds-read/README.md) (CWE-125)<br>[SQL injection](labs/cpp/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/cpp/idor/README.md) (CWE-639)<br>[Missing authorization](labs/cpp/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/cpp/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/cpp/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/cpp/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/cpp/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/cpp/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/cpp/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/cpp/business-logic/README.md) (CWE-1284)<br>[HTTP response header injection](labs/cpp/header-injection/README.md) (CWE-113)<br>[World readable secret](labs/cpp/world-readable-secret/README.md) (CWE-732)<br>[Symlink following](labs/cpp/symlink-following/README.md) (CWE-59)<br>[Heap buffer overflow](labs/cpp/heap-buffer-overflow/README.md) (CWE-122)<br>[Use after free](labs/cpp/use-after-free/README.md) (CWE-416)<br>[Double free](labs/cpp/double-free/README.md) (CWE-415)<br>[Null dereference](labs/cpp/null-dereference/README.md) (CWE-476)<br>[Stack buffer overflow](labs/cpp/stack-buffer-overflow/README.md) (CWE-121)<br>[Format string](labs/cpp/format-string/README.md) (CWE-134)<br>[Integer overflow](labs/cpp/integer-overflow/README.md) (CWE-190)<br>[Uninitialized memory](labs/cpp/uninitialized-memory/README.md) (CWE-457)<br>[Type confusion](labs/cpp/type-confusion/README.md) (CWE-843)<br>[Signed unsigned conversion](labs/cpp/signed-unsigned-conversion/README.md) (CWE-195, CWE-681) |
| [Go](labs/go/README.md) | 19 | [Cross-site scripting (XSS)](labs/go/xss/README.md) (CWE-79)<br>[Path traversal](labs/go/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/go/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/go/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/go/idor/README.md) (CWE-639)<br>[Missing authorization](labs/go/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/go/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/go/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/go/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/go/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/go/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/go/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/go/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/go/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/go/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/go/symlink-following/README.md) (CWE-59)<br>[Server-side request forgery (SSRF)](labs/go/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/go/mass-assignment/README.md) (CWE-915)<br>[Race condition](labs/go/race-condition/README.md) (CWE-362) |
| [PHP](labs/php/README.md) | 22 | [Cross-site scripting (XSS)](labs/php/xss/README.md) (CWE-79)<br>[Path traversal](labs/php/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/php/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/php/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/php/idor/README.md) (CWE-639)<br>[Missing authorization](labs/php/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/php/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/php/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/php/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/php/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/php/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/php/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/php/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/php/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/php/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/php/symlink-following/README.md) (CWE-59)<br>[Unsafe deserialization](labs/php/unsafe-deserialization/README.md) (CWE-502)<br>[XML external entities (XXE)](labs/php/xxe/README.md) (CWE-611)<br>[Server-side request forgery (SSRF)](labs/php/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/php/mass-assignment/README.md) (CWE-915)<br>[Cross-site request forgery (CSRF)](labs/php/csrf/README.md) (CWE-352)<br>[Unrestricted upload](labs/php/unrestricted-upload/README.md) (CWE-434) |
| [REST API (Python handlers)](labs/rest-api/README.md) | 42 | [Broken object-level authorization (BOLA)](labs/rest-api/bola/README.md) (CWE-639)<br>[Broken authentication](labs/rest-api/broken-authentication/README.md) (CWE-287)<br>[Property authorization](labs/rest-api/property-authorization/README.md) (CWE-915)<br>[Resource consumption](labs/rest-api/resource-consumption/README.md) (CWE-770)<br>[Function authorization](labs/rest-api/function-authorization/README.md) (CWE-862)<br>[Business flow abuse](labs/rest-api/business-flow-abuse/README.md) (CWE-799)<br>[Server-side request forgery (SSRF)](labs/rest-api/ssrf/README.md) (CWE-918)<br>[Credentialed CORS misconfiguration](labs/rest-api/cors-misconfiguration/README.md) (CWE-942)<br>[Legacy endpoint](labs/rest-api/legacy-endpoint/README.md) (CWE-489)<br>[Unsafe upstream data](labs/rest-api/unsafe-upstream-data/README.md) (CWE-20)<br>[SQL injection](labs/rest-api/sql-injection/README.md) (CWE-89)<br>[Hardcoded credentials](labs/rest-api/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/rest-api/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/rest-api/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/rest-api/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/rest-api/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/rest-api/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/rest-api/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/rest-api/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/rest-api/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/rest-api/symlink-following/README.md) (CWE-59)<br>[Cross-site scripting (XSS)](labs/rest-api/xss/README.md) (CWE-79)<br>[Path traversal](labs/rest-api/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/rest-api/command-injection/README.md) (CWE-78)<br>[Multi tenant authorization](labs/rest-api/multi-tenant-authorization/README.md) (CWE-863)<br>[Order workflow](labs/rest-api/order-workflow/README.md) (CWE-841)<br>[SSRF through an HTTP redirect](labs/rest-api/ssrf-redirect/README.md) (CWE-918)<br>[Concurrent duplicate shipment](labs/rest-api/order-concurrency/README.md) (CWE-362)<br>[Tenant cache](labs/rest-api/tenant-cache/README.md) (CWE-488)<br>[Tenant admin scope](labs/rest-api/tenant-admin-scope/README.md) (CWE-863)<br>[Tenant export worker](labs/rest-api/tenant-export-worker/README.md) (CWE-863)<br>[Tenant bulk update](labs/rest-api/tenant-bulk-update/README.md) (CWE-863)<br>[Tenant signed download](labs/rest-api/tenant-signed-download/README.md) (CWE-863)<br>[Tenant session switch](labs/rest-api/tenant-session-switch/README.md) (CWE-863)<br>[Tenant storage prefix](labs/rest-api/tenant-storage-prefix/README.md) (CWE-22)<br>[Coupon stacking](labs/rest-api/coupon-stacking/README.md) (CWE-841)<br>[Currency arbitrage](labs/rest-api/currency-arbitrage/README.md) (CWE-841, CWE-682)<br>[Split order quota](labs/rest-api/split-order-quota/README.md) (CWE-799, CWE-841)<br>[NoSQL operator injection](labs/rest-api/nosql-injection/README.md) (CWE-943)<br>[GraphQL depth amplification and introspection](labs/rest-api/graphql-depth-amplification/README.md) (CWE-400, CWE-200)<br>[User enumeration](labs/rest-api/user-enumeration/README.md) (CWE-203, CWE-208)<br>[Web cache poisoning](labs/rest-api/web-cache-poisoning/README.md) (CWE-525, CWE-444) |
| [Node.js](labs/node/README.md) | 27 | [Cross-site scripting (XSS)](labs/node/xss/README.md) (CWE-79)<br>[Path traversal](labs/node/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/node/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/node/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/node/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/node/idor/README.md) (CWE-639)<br>[Missing authorization](labs/node/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/node/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/node/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/node/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/node/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/node/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/node/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/node/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/node/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/node/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/node/symlink-following/README.md) (CWE-59)<br>[Vulnerable dependency](labs/node/vulnerable-dependency/README.md) (CWE-1395)<br>[Vulnerable transitive dependency](labs/node/vulnerable-transitive-dependency/README.md) (CWE-1395)<br>[Partial HMAC comparison](labs/node/partial-signature/README.md) (CWE-187)<br>[Client-controlled price](labs/node/client-price/README.md) (CWE-602)<br>[Permissive origin regex](labs/node/regex-origin/README.md) (CWE-625)<br>[Signed action replay](labs/node/signed-action-replay/README.md) (CWE-294)<br>[Unsafe deserialization](labs/node/unsafe-deserialization/README.md) (CWE-502)<br>[XML external entities (XXE)](labs/node/xxe/README.md) (CWE-611)<br>[Server-side request forgery (SSRF)](labs/node/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/node/mass-assignment/README.md) (CWE-915) |
| [Python](labs/python/README.md) | 83 | [Cross-site scripting (XSS)](labs/python/xss/README.md) (CWE-79)<br>[Path traversal](labs/python/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/python/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/python/sql-injection/README.md) (CWE-89)<br>[Code injection](labs/python/code-injection/README.md) (CWE-95)<br>[Unsafe deserialization](labs/python/unsafe-deserialization/README.md) (CWE-502)<br>[Insecure direct object reference (IDOR)](labs/python/idor/README.md) (CWE-639)<br>[Mass assignment](labs/python/mass-assignment/README.md) (CWE-915)<br>[Cross-site request forgery (CSRF)](labs/python/csrf/README.md) (CWE-352)<br>[Session fixation](labs/python/session-fixation/README.md) (CWE-384)<br>[Weak password hash](labs/python/weak-password-hash/README.md) (CWE-916)<br>[Hardcoded credentials](labs/python/hardcoded-credentials/README.md) (CWE-798)<br>[Predictable token](labs/python/predictable-token/README.md) (CWE-330)<br>[Log injection](labs/python/log-injection/README.md) (CWE-117)<br>[Sensitive logging](labs/python/sensitive-logging/README.md) (CWE-532)<br>[Error disclosure](labs/python/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/python/fail-open/README.md) (CWE-636)<br>[Unverified update](labs/python/unverified-update/README.md) (CWE-494)<br>[Untrusted plugin](labs/python/untrusted-plugin/README.md) (CWE-829)<br>[Open redirect](labs/python/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/python/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/python/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/python/world-readable-secret/README.md) (CWE-732)<br>[Disabled TLS verification](labs/python/tls-verification/README.md) (CWE-295)<br>[Missing security audit events](labs/python/missing-audit/README.md) (CWE-778)<br>[Missing authorization](labs/python/missing-authorization/README.md) (CWE-862)<br>[HTTP response header injection](labs/python/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/python/symlink-following/README.md) (CWE-59)<br>[SQL injection in an ORDER BY identifier](labs/python/sql-order-by/README.md) (CWE-89)<br>[Second-order SQL injection](labs/python/sql-second-order/README.md) (CWE-89)<br>[XSS in an HTML attribute](labs/python/xss-attribute/README.md) (CWE-79)<br>[Sql login bypass](labs/python/sql-login-bypass/README.md) (CWE-89)<br>[Zip slip](labs/python/zip-slip/README.md) (CWE-22)<br>[Password reset host](labs/python/password-reset-host/README.md) (CWE-346)<br>[Unrestricted upload](labs/python/unrestricted-upload/README.md) (CWE-434)<br>[XML external entities (XXE)](labs/python/xxe/README.md) (CWE-611)<br>[Jwt default key](labs/python/jwt-default-key/README.md) (CWE-321)<br>[Jwt disabled user](labs/python/jwt-disabled-user/README.md) (CWE-863)<br>[Csv formula injection](labs/python/csv-formula-injection/README.md) (CWE-1236)<br>[Argument injection](labs/python/argument-injection/README.md) (CWE-88)<br>[Format string disclosure](labs/python/format-string-disclosure/README.md) (CWE-134)<br>[File create race](labs/python/file-create-race/README.md) (CWE-367)<br>[Json parser conflict](labs/python/json-parser-conflict/README.md) (CWE-436)<br>[Unicode path validation](labs/python/unicode-path-validation/README.md) (CWE-180)<br>[Password reset replay](labs/python/password-reset-replay/README.md) (CWE-640)<br>[Webhook signature](labs/python/webhook-signature/README.md) (CWE-347)<br>[Decompression amplification](labs/python/decompression-amplification/README.md) (CWE-409)<br>[Session expiration](labs/python/session-expiration/README.md) (CWE-613)<br>[Partial HMAC comparison](labs/python/partial-signature/README.md) (CWE-187)<br>[Client-controlled price](labs/python/client-price/README.md) (CWE-602)<br>[Permissive origin regex](labs/python/regex-origin/README.md) (CWE-625)<br>[Signed action replay](labs/python/signed-action-replay/README.md) (CWE-294)<br>[Double-decoding path traversal](labs/python/double-decoding-traversal/README.md) (CWE-22)<br>[Item-name template injection](labs/python/item-template-injection/README.md) (CWE-1336)<br>[CGI redirect response splitting](labs/python/cgi-redirect-splitting/README.md) (CWE-113)<br>[DNS rebinding SSRF](labs/python/dns-rebinding-ssrf/README.md) (CWE-918)<br>[SVG resource SSRF](labs/python/svg-resource-ssrf/README.md) (CWE-918)<br>[Remote-file import SSRF](labs/python/remote-import-ssrf/README.md) (CWE-918)<br>[TAR symlink escape](labs/python/tar-symlink-escape/README.md) (CWE-59)<br>[Factory authentication bypass](labs/python/factory-auth-bypass/README.md) (CWE-288)<br>[Query-clause authorization bypass](labs/python/query-clause-authorization/README.md) (CWE-863)<br>[Backslash open redirect](labs/python/backslash-open-redirect/README.md) (CWE-601)<br>[Log4Shell: message lookup injection](labs/python/log4shell-lookup/README.md) (CWE-917)<br>[TeamCity: dispatch authentication bypass](labs/python/teamcity-dispatch-bypass/README.md) (CWE-288)<br>[Confluence: pre-auth expression evaluation](labs/python/confluence-expression-dispatch/README.md) (CWE-917)<br>[Spring4Shell: class-loader property binding](labs/python/spring4shell-binding/README.md) (CWE-915)<br>[Jenkins CLI: pre-auth file expansion](labs/python/jenkins-cli-atfile/README.md) (CWE-73)<br>[FortiOS: forwarded-header authentication bypass](labs/python/fortios-forwarded-auth/README.md) (CWE-288)<br>[Confluence: setup-state binding](labs/python/confluence-setup-reopen/README.md) (CWE-915)<br>[GitLab: unverified reset recipients](labs/python/gitlab-reset-recipients/README.md) (CWE-640)<br>[MinIO: bootstrap credential disclosure](labs/python/minio-bootstrap-disclosure/README.md) (CWE-306)<br>[ActiveMQ: unchecked throwable construction](labs/python/activemq-openwire-type/README.md) (CWE-470)<br>[Zabbix: role projection SQL injection](labs/python/zabbix-role-projection/README.md) (CWE-89)<br>[ImageTragick: delegate shell injection](labs/python/imagetragick-delegate/README.md) (CWE-78)<br>[Apache HTTP Server: proxy request splitting](labs/python/apache-proxy-request-splitting/README.md) (CWE-444)<br>[Monetary rounding](labs/python/monetary-rounding/README.md) (CWE-1339, CWE-682)<br>[LDAP filter injection](labs/python/ldap-injection/README.md) (CWE-90)<br>[XPath predicate injection](labs/python/xpath-injection/README.md) (CWE-643)<br>[XML entity expansion (Billion Laughs)](labs/python/xml-entity-expansion/README.md) (CWE-776)<br>[Regular expression denial of service (ReDoS)](labs/python/redos/README.md) (CWE-1333)<br>[JWT algorithm confusion](labs/python/jwt-alg-confusion/README.md) (CWE-347)<br>[Cryptographic stream-cipher nonce reuse](labs/python/crypto-nonce-reuse/README.md) (CWE-323, CWE-329, CWE-327)<br>[Weak PRNG token generation](labs/python/weak-prng-token/README.md) (CWE-338) |
| [CGI (Python)](labs/cgi/README.md) | 17 | [Cross-site scripting (XSS)](labs/cgi/xss/README.md) (CWE-79)<br>[HTTP response header injection](labs/cgi/header-injection/README.md) (CWE-113)<br>[SQL injection](labs/cgi/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/cgi/idor/README.md) (CWE-639)<br>[Missing authorization](labs/cgi/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/cgi/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/cgi/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/cgi/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/cgi/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/cgi/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/cgi/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/cgi/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/cgi/world-readable-secret/README.md) (CWE-732)<br>[Symlink following](labs/cgi/symlink-following/README.md) (CWE-59)<br>[Path traversal](labs/cgi/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/cgi/command-injection/README.md) (CWE-78)<br>[Insecure cookie flags](labs/cgi/insecure-cookie-flags/README.md) (CWE-614, CWE-1004, CWE-1275) |
| [.NET / C#](labs/dotnet/README.md) | 20 | [Cross-site scripting (XSS)](labs/dotnet/xss/README.md) (CWE-79)<br>[Path traversal](labs/dotnet/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/dotnet/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/dotnet/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/dotnet/idor/README.md) (CWE-639)<br>[Missing authorization](labs/dotnet/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/dotnet/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/dotnet/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/dotnet/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/dotnet/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/dotnet/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/dotnet/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/dotnet/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/dotnet/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/dotnet/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/dotnet/symlink-following/README.md) (CWE-59)<br>[Unsafe deserialization](labs/dotnet/unsafe-deserialization/README.md) (CWE-502)<br>[XML external entities (XXE)](labs/dotnet/xxe/README.md) (CWE-611)<br>[Server-side request forgery (SSRF)](labs/dotnet/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/dotnet/mass-assignment/README.md) (CWE-915) |
| [TypeScript](labs/typescript/README.md) | 19 | [Cross-site scripting (XSS)](labs/typescript/xss/README.md) (CWE-79)<br>[Path traversal](labs/typescript/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/typescript/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/typescript/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/typescript/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/typescript/idor/README.md) (CWE-639)<br>[Missing authorization](labs/typescript/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/typescript/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/typescript/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/typescript/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/typescript/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/typescript/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/typescript/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/typescript/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/typescript/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/typescript/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/typescript/symlink-following/README.md) (CWE-59)<br>[Server-side request forgery (SSRF)](labs/typescript/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/typescript/mass-assignment/README.md) (CWE-915) |
| [Java](labs/java/README.md) | 20 | [Cross-site scripting (XSS)](labs/java/xss/README.md) (CWE-79)<br>[Path traversal](labs/java/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/java/command-injection/README.md) (CWE-78)<br>[XML external entities (XXE)](labs/java/xxe/README.md) (CWE-611)<br>[SQL injection](labs/java/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/java/idor/README.md) (CWE-639)<br>[Missing authorization](labs/java/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/java/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/java/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/java/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/java/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/java/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/java/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/java/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/java/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/java/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/java/symlink-following/README.md) (CWE-59)<br>[Unsafe deserialization](labs/java/unsafe-deserialization/README.md) (CWE-502)<br>[Server-side request forgery (SSRF)](labs/java/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/java/mass-assignment/README.md) (CWE-915) |
| [Ruby](labs/ruby/README.md) | 20 | [Cross-site scripting (XSS)](labs/ruby/xss/README.md) (CWE-79)<br>[Path traversal](labs/ruby/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/ruby/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/ruby/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/ruby/idor/README.md) (CWE-639)<br>[Missing authorization](labs/ruby/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/ruby/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/ruby/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/ruby/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/ruby/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/ruby/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/ruby/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/ruby/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/ruby/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/ruby/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/ruby/symlink-following/README.md) (CWE-59)<br>[Unsafe deserialization](labs/ruby/unsafe-deserialization/README.md) (CWE-502)<br>[XML external entities (XXE)](labs/ruby/xxe/README.md) (CWE-611)<br>[Server-side request forgery (SSRF)](labs/ruby/ssrf/README.md) (CWE-918)<br>[Mass assignment](labs/ruby/mass-assignment/README.md) (CWE-915) |
| [Rust](labs/rust/README.md) | 18 | [Cross-site scripting (XSS)](labs/rust/xss/README.md) (CWE-79)<br>[Path traversal](labs/rust/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/rust/command-injection/README.md) (CWE-78)<br>[Integer overflow](labs/rust/integer-overflow/README.md) (CWE-190)<br>[SQL injection](labs/rust/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/rust/idor/README.md) (CWE-639)<br>[Missing authorization](labs/rust/missing-authorization/README.md) (CWE-862)<br>[Hardcoded credentials](labs/rust/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/rust/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/rust/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/rust/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/rust/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/rust/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/rust/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/rust/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/rust/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/rust/symlink-following/README.md) (CWE-59)<br>[Unsafe slice bounds](labs/rust/unsafe-slice-bounds/README.md) (CWE-119, CWE-125) |
| [AI / LLM boundaries](labs/ai/README.md) | 30 | [Prompt trust boundary](labs/ai/prompt-trust-boundary/README.md) (CWE-1427)<br>[Sensitive context](labs/ai/sensitive-context/README.md) (CWE-200)<br>[Model artifact integrity](labs/ai/model-artifact-integrity/README.md) (CWE-494)<br>[Training data poisoning](labs/ai/training-data-poisoning/README.md) (CWE-20)<br>[Unsafe model output](labs/ai/unsafe-model-output/README.md) (CWE-79)<br>[Excessive agency](labs/ai/excessive-agency/README.md) (CWE-862)<br>[System prompt leakage](labs/ai/system-prompt-leakage/README.md) (CWE-200)<br>[Cross tenant retrieval](labs/ai/cross-tenant-retrieval/README.md) (CWE-863)<br>[Unverified security claim](labs/ai/unverified-security-claim/README.md) (CWE-345)<br>[Unbounded agent loop](labs/ai/unbounded-agent-loop/README.md) (CWE-834)<br>[SQL injection](labs/ai/sql-injection/README.md) (CWE-89)<br>[Insecure direct object reference (IDOR)](labs/ai/idor/README.md) (CWE-639)<br>[Hardcoded credentials](labs/ai/hardcoded-credentials/README.md) (CWE-798)<br>[Log injection](labs/ai/log-injection/README.md) (CWE-117)<br>[Error disclosure](labs/ai/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/ai/fail-open/README.md) (CWE-636)<br>[Open redirect](labs/ai/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/ai/unbounded-work/README.md) (CWE-400)<br>[Invalid purchase quantity](labs/ai/business-logic/README.md) (CWE-1284)<br>[World readable secret](labs/ai/world-readable-secret/README.md) (CWE-732)<br>[HTTP response header injection](labs/ai/header-injection/README.md) (CWE-113)<br>[Symlink following](labs/ai/symlink-following/README.md) (CWE-59)<br>[Path traversal](labs/ai/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/ai/command-injection/README.md) (CWE-78)<br>[Tool argument scope](labs/ai/tool-argument-scope/README.md) (CWE-863)<br>[MCP tool description poisoning](labs/ai/mcp-tool-poisoning/README.md) (CWE-1427)<br>[Markdown image exfiltration](labs/ai/markdown-image-exfiltration/README.md) (CWE-200)<br>[HITL approval TOCTOU bypass](labs/ai/hitl-approval-toctou/README.md) (CWE-367)<br>[Memory poisoning](labs/ai/memory-poisoning/README.md) (CWE-472)<br>[Agent connector SSRF](labs/ai/agent-connector-ssrf/README.md) (CWE-918) |

## What coverage means

The [complete CWE matrix](docs/CWE-MATRIX.md) enumerates all **1450 entries** from MITRE CWE
**4.20**: **969 weaknesses** plus categories and views. **102 weaknesses** currently
have direct executable cases; **867 remain explicit gaps**. Categories and views are marked
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

## Training corpus

The [deduplicated JSONL training file](enrichissement/vulnerabilities.training.jsonl) contains English
vulnerable/fixed detection and repair conversations for every catalog case. Each record contains
only a `messages` array. Identical conversations shared by cases are included once.
Examples use the current sources and local build/configuration companions, with the case scope
and remediation from the catalog. Training labels come from fixture contracts; inclusion does
not certify runtime execution or reproduction of a referenced product vulnerability.

Regenerate after source or catalog changes, then verify freshness without writing:

```sh
python3 tools/export_training.py
python3 tools/export_training.py --check
```

## Repository layout

```text
catalog/       Case contracts, CWE snapshot, OWASP references and AI attack manifest
labs/          One section per technology; vulnerable/ and fixed/ source pairs
tools/         Regression runner, scorer, CWE importer and documentation renderer
tests/         Regression tests for the benchmark tooling itself
docs/          Complete CWE matrix, OWASP mappings and evaluation protocols
enrichissement/ English training dataset (JSONL)
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
