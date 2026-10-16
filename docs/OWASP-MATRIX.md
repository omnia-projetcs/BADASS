# OWASP coverage matrix

Project-maintained mappings to pinned editions. A mapped example is not exhaustive category coverage.
Scope distinguishes executable sinks, handler models, configuration checks and AI application boundaries.

Other OWASP projects, including ASVS and WSTG, are not claimed as fully covered.

## owasp-web-2025

[Official reference](https://top10.owasp.org/2025/0x00_2025-Introduction/)

| Category | Title | Cases and scopes |
|---|---|---|
| A01:2025 | Broken Access Control | [python/path-traversal](../labs/python/path-traversal/README.md) — executable<br>[node/path-traversal](../labs/node/path-traversal/README.md) — executable<br>[typescript/path-traversal](../labs/typescript/path-traversal/README.md) — executable<br>[php/path-traversal](../labs/php/path-traversal/README.md) — executable<br>[ruby/path-traversal](../labs/ruby/path-traversal/README.md) — executable<br>[go/path-traversal](../labs/go/path-traversal/README.md) — executable<br>[java/path-traversal](../labs/java/path-traversal/README.md) — executable<br>[rust/path-traversal](../labs/rust/path-traversal/README.md) — executable<br>[c/path-traversal](../labs/c/path-traversal/README.md) — executable<br>[cpp/path-traversal](../labs/cpp/path-traversal/README.md) — executable<br>[dotnet/path-traversal](../labs/dotnet/path-traversal/README.md) — executable<br>[python/idor](../labs/python/idor/README.md) — executable<br>[python/mass-assignment](../labs/python/mass-assignment/README.md) — executable<br>[python/csrf](../labs/python/csrf/README.md) — handler-unit<br>[python/open-redirect](../labs/python/open-redirect/README.md) — executable<br>[python/world-readable-secret](../labs/python/world-readable-secret/README.md) — executable |
| A02:2025 | Security Misconfiguration | [java/xxe](../labs/java/xxe/README.md) — executable<br>[python/error-disclosure](../labs/python/error-disclosure/README.md) — executable |
| A03:2025 | Software Supply Chain Failures | [python/untrusted-plugin](../labs/python/untrusted-plugin/README.md) — executable |
| A04:2025 | Cryptographic Failures | [python/weak-password-hash](../labs/python/weak-password-hash/README.md) — executable<br>[python/tls-verification](../labs/python/tls-verification/README.md) — configuration-unit |
| A05:2025 | Injection | [python/xss](../labs/python/xss/README.md) — executable<br>[python/command-injection](../labs/python/command-injection/README.md) — executable<br>[node/xss](../labs/node/xss/README.md) — executable<br>[node/command-injection](../labs/node/command-injection/README.md) — executable<br>[typescript/xss](../labs/typescript/xss/README.md) — executable<br>[typescript/command-injection](../labs/typescript/command-injection/README.md) — executable<br>[php/xss](../labs/php/xss/README.md) — executable<br>[php/command-injection](../labs/php/command-injection/README.md) — executable<br>[ruby/xss](../labs/ruby/xss/README.md) — executable<br>[ruby/command-injection](../labs/ruby/command-injection/README.md) — executable<br>[go/xss](../labs/go/xss/README.md) — executable<br>[go/command-injection](../labs/go/command-injection/README.md) — executable<br>[java/xss](../labs/java/xss/README.md) — executable<br>[java/command-injection](../labs/java/command-injection/README.md) — executable<br>[rust/xss](../labs/rust/xss/README.md) — executable<br>[rust/command-injection](../labs/rust/command-injection/README.md) — executable<br>[c/xss](../labs/c/xss/README.md) — executable<br>[c/command-injection](../labs/c/command-injection/README.md) — executable<br>[cpp/xss](../labs/cpp/xss/README.md) — executable<br>[cpp/command-injection](../labs/cpp/command-injection/README.md) — executable<br>[dotnet/xss](../labs/dotnet/xss/README.md) — executable<br>[dotnet/command-injection](../labs/dotnet/command-injection/README.md) — executable<br>[cgi/xss](../labs/cgi/xss/README.md) — executable<br>[cgi/header-injection](../labs/cgi/header-injection/README.md) — executable<br>[c/format-string](../labs/c/format-string/README.md) — executable<br>[python/sql-injection](../labs/python/sql-injection/README.md) — executable<br>[python/code-injection](../labs/python/code-injection/README.md) — executable |
| A06:2025 | Insecure Design | [c/stack-buffer-overflow](../labs/c/stack-buffer-overflow/README.md) — executable<br>[cpp/out-of-bounds-read](../labs/cpp/out-of-bounds-read/README.md) — executable<br>[rust/integer-overflow](../labs/rust/integer-overflow/README.md) — executable<br>[python/unbounded-work](../labs/python/unbounded-work/README.md) — executable<br>[python/business-logic](../labs/python/business-logic/README.md) — executable |
| A07:2025 | Authentication Failures | [python/session-fixation](../labs/python/session-fixation/README.md) — executable<br>[python/hardcoded-credentials](../labs/python/hardcoded-credentials/README.md) — executable<br>[python/predictable-token](../labs/python/predictable-token/README.md) — executable |
| A08:2025 | Software or Data Integrity Failures | [node/prototype-pollution](../labs/node/prototype-pollution/README.md) — executable<br>[typescript/prototype-pollution](../labs/typescript/prototype-pollution/README.md) — executable<br>[python/unsafe-deserialization](../labs/python/unsafe-deserialization/README.md) — executable<br>[python/unverified-update](../labs/python/unverified-update/README.md) — executable |
| A09:2025 | Security Logging and Alerting Failures | [python/log-injection](../labs/python/log-injection/README.md) — executable<br>[python/sensitive-logging](../labs/python/sensitive-logging/README.md) — executable<br>[python/missing-audit](../labs/python/missing-audit/README.md) — handler-unit |
| A10:2025 | Mishandling of Exceptional Conditions | [python/fail-open](../labs/python/fail-open/README.md) — executable |

## owasp-api-2023

[Official reference](https://api-security.owasp.org/editions/2023/en/0x11-t10/)

| Category | Title | Cases and scopes |
|---|---|---|
| API1:2023 | Broken Object Level Authorization | [rest-api/bola](../labs/rest-api/bola/README.md) — handler-unit |
| API2:2023 | Broken Authentication | [rest-api/broken-authentication](../labs/rest-api/broken-authentication/README.md) — handler-unit |
| API3:2023 | Broken Object Property Level Authorization | [rest-api/property-authorization](../labs/rest-api/property-authorization/README.md) — handler-unit |
| API4:2023 | Unrestricted Resource Consumption | [rest-api/resource-consumption](../labs/rest-api/resource-consumption/README.md) — handler-unit |
| API5:2023 | Broken Function Level Authorization | [rest-api/function-authorization](../labs/rest-api/function-authorization/README.md) — handler-unit |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | [rest-api/business-flow-abuse](../labs/rest-api/business-flow-abuse/README.md) — state-machine-unit |
| API7:2023 | Server Side Request Forgery | [rest-api/ssrf](../labs/rest-api/ssrf/README.md) — loopback-integration |
| API8:2023 | Security Misconfiguration | [rest-api/cors-misconfiguration](../labs/rest-api/cors-misconfiguration/README.md) — handler-unit |
| API9:2023 | Improper Inventory Management | [rest-api/legacy-endpoint](../labs/rest-api/legacy-endpoint/README.md) — handler-unit |
| API10:2023 | Unsafe Consumption of APIs | [rest-api/unsafe-upstream-data](../labs/rest-api/unsafe-upstream-data/README.md) — handler-unit |

## owasp-llm-2025

[Official reference](https://genai.owasp.org/llm-top-10/)

| Category | Title | Cases and scopes |
|---|---|---|
| LLM01:2025 | Prompt Injection | [ai/prompt-trust-boundary](../labs/ai/prompt-trust-boundary/README.md) — ai-boundary-unit |
| LLM02:2025 | Sensitive Information Disclosure | [ai/sensitive-context](../labs/ai/sensitive-context/README.md) — ai-boundary-unit |
| LLM03:2025 | Supply Chain | [ai/model-artifact-integrity](../labs/ai/model-artifact-integrity/README.md) — ai-boundary-unit |
| LLM04:2025 | Data and Model Poisoning | [ai/training-data-poisoning](../labs/ai/training-data-poisoning/README.md) — ai-boundary-unit |
| LLM05:2025 | Improper Output Handling | [ai/unsafe-model-output](../labs/ai/unsafe-model-output/README.md) — ai-boundary-unit |
| LLM06:2025 | Excessive Agency | [ai/excessive-agency](../labs/ai/excessive-agency/README.md) — ai-boundary-unit |
| LLM07:2025 | System Prompt Leakage | [ai/system-prompt-leakage](../labs/ai/system-prompt-leakage/README.md) — ai-boundary-unit |
| LLM08:2025 | Vector and Embedding Weaknesses | [ai/cross-tenant-retrieval](../labs/ai/cross-tenant-retrieval/README.md) — ai-boundary-unit |
| LLM09:2025 | Misinformation | [ai/unverified-security-claim](../labs/ai/unverified-security-claim/README.md) — ai-boundary-unit |
| LLM10:2025 | Unbounded Consumption | [ai/unbounded-agent-loop](../labs/ai/unbounded-agent-loop/README.md) — ai-boundary-unit |
