# BADASS

**Broken Application Designed for Auditing Security Scanners**

An executable security benchmark for validating vulnerability detection and remediation across languages,
REST APIs, CGI handlers and AI-assisted audit workflows. Each case includes deliberately vulnerable
code, a corrected counterpart, benign inputs, attack inputs and machine-readable expectations.

**97 case pairs · 14 technology sections · 45 distinct CWE weaknesses · 30 OWASP categories represented**

This is a local laboratory containing intentional vulnerabilities. Use synthetic data and the isolated
container workflow. No service is exposed publicly, and no real credentials or external model calls are required.

## Quick start

```sh
# Validate metadata and run the Python section with the installed runtime.
python3 tools/lab.py validate
python3 tools/lab.py test --language python --strict

# Build all runtimes, then run every case with external networking disabled.
make container-build
make container-test
```

Python 3.11+ is sufficient for the tooling, Python, CGI, REST API and AI boundary sections.
The full Linux suite uses GCC/G++, Go, PHP 8+, Node.js, TypeScript, .NET 8 SDK, JDK 17+, Ruby and Rust.
Docker installs these runtimes without changing your host installation. The first image build needs network access.
The container regression report is written to `reports/container-regression.json`.

**SQL injection (CWE-89) is implemented in every technology section**, using actual in-memory SQLite queries
and parameter-bound corrections. The image includes the required language drivers.
Run all SQL injection cases with:

```sh
make container-test LAB_ARGS='test --cwe CWE-89 --strict --output reports/sql-injection.json'
```

See [SQL injection cases, drivers and test coverage](docs/SQL-INJECTION.md).

## Vulnerabilities by technology

Every vulnerability currently implemented is listed below. Links open the case documentation, including
the vulnerable and corrected source files. A case in the table is not a claim of full CWE coverage.

| Technology | Cases | Implemented vulnerabilities (CWE) |
|---|---:|---|
| [C](labs/c/README.md) | 6 | [Cross-site scripting (XSS)](labs/c/xss/README.md) (CWE-79)<br>[Path traversal](labs/c/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/c/command-injection/README.md) (CWE-78)<br>[Stack buffer overflow](labs/c/stack-buffer-overflow/README.md) (CWE-121)<br>[Format string](labs/c/format-string/README.md) (CWE-134)<br>[SQL injection](labs/c/sql-injection/README.md) (CWE-89) |
| [C++](labs/cpp/README.md) | 5 | [Cross-site scripting (XSS)](labs/cpp/xss/README.md) (CWE-79)<br>[Path traversal](labs/cpp/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/cpp/command-injection/README.md) (CWE-78)<br>[Out of bounds read](labs/cpp/out-of-bounds-read/README.md) (CWE-125)<br>[SQL injection](labs/cpp/sql-injection/README.md) (CWE-89) |
| [Go](labs/go/README.md) | 4 | [Cross-site scripting (XSS)](labs/go/xss/README.md) (CWE-79)<br>[Path traversal](labs/go/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/go/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/go/sql-injection/README.md) (CWE-89) |
| [PHP](labs/php/README.md) | 4 | [Cross-site scripting (XSS)](labs/php/xss/README.md) (CWE-79)<br>[Path traversal](labs/php/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/php/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/php/sql-injection/README.md) (CWE-89) |
| [REST API (Python handlers)](labs/rest-api/README.md) | 11 | [Broken object-level authorization (BOLA)](labs/rest-api/bola/README.md) (CWE-639)<br>[Broken authentication](labs/rest-api/broken-authentication/README.md) (CWE-287)<br>[Property authorization](labs/rest-api/property-authorization/README.md) (CWE-915)<br>[Resource consumption](labs/rest-api/resource-consumption/README.md) (CWE-770)<br>[Function authorization](labs/rest-api/function-authorization/README.md) (CWE-862)<br>[Business flow abuse](labs/rest-api/business-flow-abuse/README.md) (CWE-799)<br>[Server-side request forgery (SSRF)](labs/rest-api/ssrf/README.md) (CWE-918)<br>[Credentialed CORS misconfiguration](labs/rest-api/cors-misconfiguration/README.md) (CWE-942)<br>[Legacy endpoint](labs/rest-api/legacy-endpoint/README.md) (CWE-489)<br>[Unsafe upstream data](labs/rest-api/unsafe-upstream-data/README.md) (CWE-20)<br>[SQL injection](labs/rest-api/sql-injection/README.md) (CWE-89) |
| [Node.js](labs/node/README.md) | 5 | [Cross-site scripting (XSS)](labs/node/xss/README.md) (CWE-79)<br>[Path traversal](labs/node/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/node/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/node/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/node/sql-injection/README.md) (CWE-89) |
| [Python](labs/python/README.md) | 25 | [Cross-site scripting (XSS)](labs/python/xss/README.md) (CWE-79)<br>[Path traversal](labs/python/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/python/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/python/sql-injection/README.md) (CWE-89)<br>[Code injection](labs/python/code-injection/README.md) (CWE-95)<br>[Unsafe deserialization](labs/python/unsafe-deserialization/README.md) (CWE-502)<br>[Insecure direct object reference (IDOR)](labs/python/idor/README.md) (CWE-639)<br>[Mass assignment](labs/python/mass-assignment/README.md) (CWE-915)<br>[Cross-site request forgery (CSRF)](labs/python/csrf/README.md) (CWE-352)<br>[Session fixation](labs/python/session-fixation/README.md) (CWE-384)<br>[Weak password hash](labs/python/weak-password-hash/README.md) (CWE-916)<br>[Hardcoded credentials](labs/python/hardcoded-credentials/README.md) (CWE-798)<br>[Predictable token](labs/python/predictable-token/README.md) (CWE-330)<br>[Log injection](labs/python/log-injection/README.md) (CWE-117)<br>[Sensitive logging](labs/python/sensitive-logging/README.md) (CWE-532)<br>[Error disclosure](labs/python/error-disclosure/README.md) (CWE-209)<br>[Fail open](labs/python/fail-open/README.md) (CWE-636)<br>[Unverified update](labs/python/unverified-update/README.md) (CWE-494)<br>[Untrusted plugin](labs/python/untrusted-plugin/README.md) (CWE-829)<br>[Open redirect](labs/python/open-redirect/README.md) (CWE-601)<br>[Unbounded work](labs/python/unbounded-work/README.md) (CWE-400)<br>[Business logic](labs/python/business-logic/README.md) (CWE-841)<br>[World readable secret](labs/python/world-readable-secret/README.md) (CWE-732)<br>[Disabled TLS verification](labs/python/tls-verification/README.md) (CWE-295)<br>[Missing security audit events](labs/python/missing-audit/README.md) (CWE-778) |
| [CGI (Python)](labs/cgi/README.md) | 3 | [Cross-site scripting (XSS)](labs/cgi/xss/README.md) (CWE-79)<br>[HTTP response header injection](labs/cgi/header-injection/README.md) (CWE-113)<br>[SQL injection](labs/cgi/sql-injection/README.md) (CWE-89) |
| [.NET / C#](labs/dotnet/README.md) | 4 | [Cross-site scripting (XSS)](labs/dotnet/xss/README.md) (CWE-79)<br>[Path traversal](labs/dotnet/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/dotnet/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/dotnet/sql-injection/README.md) (CWE-89) |
| [TypeScript](labs/typescript/README.md) | 5 | [Cross-site scripting (XSS)](labs/typescript/xss/README.md) (CWE-79)<br>[Path traversal](labs/typescript/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/typescript/command-injection/README.md) (CWE-78)<br>[Prototype pollution](labs/typescript/prototype-pollution/README.md) (CWE-1321)<br>[SQL injection](labs/typescript/sql-injection/README.md) (CWE-89) |
| [Java](labs/java/README.md) | 5 | [Cross-site scripting (XSS)](labs/java/xss/README.md) (CWE-79)<br>[Path traversal](labs/java/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/java/command-injection/README.md) (CWE-78)<br>[XML external entities (XXE)](labs/java/xxe/README.md) (CWE-611)<br>[SQL injection](labs/java/sql-injection/README.md) (CWE-89) |
| [Ruby](labs/ruby/README.md) | 4 | [Cross-site scripting (XSS)](labs/ruby/xss/README.md) (CWE-79)<br>[Path traversal](labs/ruby/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/ruby/command-injection/README.md) (CWE-78)<br>[SQL injection](labs/ruby/sql-injection/README.md) (CWE-89) |
| [Rust](labs/rust/README.md) | 5 | [Cross-site scripting (XSS)](labs/rust/xss/README.md) (CWE-79)<br>[Path traversal](labs/rust/path-traversal/README.md) (CWE-22)<br>[Command injection](labs/rust/command-injection/README.md) (CWE-78)<br>[Integer overflow](labs/rust/integer-overflow/README.md) (CWE-190)<br>[SQL injection](labs/rust/sql-injection/README.md) (CWE-89) |
| [AI / LLM boundaries](labs/ai/README.md) | 11 | [Prompt trust boundary](labs/ai/prompt-trust-boundary/README.md) (CWE-1427)<br>[Sensitive context](labs/ai/sensitive-context/README.md) (CWE-200)<br>[Model artifact integrity](labs/ai/model-artifact-integrity/README.md) (CWE-494)<br>[Training data poisoning](labs/ai/training-data-poisoning/README.md) (CWE-20)<br>[Unsafe model output](labs/ai/unsafe-model-output/README.md) (CWE-79)<br>[Excessive agency](labs/ai/excessive-agency/README.md) (CWE-862)<br>[System prompt leakage](labs/ai/system-prompt-leakage/README.md) (CWE-200)<br>[Cross tenant retrieval](labs/ai/cross-tenant-retrieval/README.md) (CWE-863)<br>[Unverified security claim](labs/ai/unverified-security-claim/README.md) (CWE-345)<br>[Unbounded agent loop](labs/ai/unbounded-agent-loop/README.md) (CWE-834)<br>[SQL injection](labs/ai/sql-injection/README.md) (CWE-89) |

## What coverage means

The [complete CWE matrix](docs/CWE-MATRIX.md) enumerates all **1450 entries** from MITRE CWE
**4.20**: **969 weaknesses** plus categories and views. **45 weaknesses** currently
have direct executable cases; **924 remain explicit gaps**. Categories and views are marked
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
.github/       CI validation and full isolated regression workflow
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
