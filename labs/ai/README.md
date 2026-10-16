# AI / LLM boundaries

[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)

```sh
python3 tools/lab.py test --language ai --strict
```

Run commands from the repository root. Cases are independent and use synthetic fixtures.

| Vulnerability | CWE | OWASP | Scope |
|---|---|---|---|
| [Prompt trust boundary](prompt-trust-boundary/README.md) | CWE-1427 | LLM01:2025 | ai-boundary-unit |
| [Sensitive context](sensitive-context/README.md) | CWE-200 | LLM02:2025 | ai-boundary-unit |
| [Model artifact integrity](model-artifact-integrity/README.md) | CWE-494 | LLM03:2025 | ai-boundary-unit |
| [Training data poisoning](training-data-poisoning/README.md) | CWE-20 | LLM04:2025 | ai-boundary-unit |
| [Unsafe model output](unsafe-model-output/README.md) | CWE-79 | LLM05:2025 | ai-boundary-unit |
| [Excessive agency](excessive-agency/README.md) | CWE-862 | LLM06:2025 | ai-boundary-unit |
| [System prompt leakage](system-prompt-leakage/README.md) | CWE-200 | LLM07:2025 | ai-boundary-unit |
| [Cross tenant retrieval](cross-tenant-retrieval/README.md) | CWE-863 | LLM08:2025 | ai-boundary-unit |
| [Unverified security claim](unverified-security-claim/README.md) | CWE-345 | LLM09:2025 | ai-boundary-unit |
| [Unbounded agent loop](unbounded-agent-loop/README.md) | CWE-834 | LLM10:2025 | ai-boundary-unit |
| [SQL injection](sql-injection/README.md) | CWE-89 | A05:2025, LLM05:2025 | ai-boundary-unit |
| [Insecure direct object reference (IDOR)](idor/README.md) | CWE-639 | A01:2025 | handler-unit |
| [Hardcoded credentials](hardcoded-credentials/README.md) | CWE-798 | A07:2025 | handler-unit |
| [Log injection](log-injection/README.md) | CWE-117 | A09:2025 | executable |
| [Error disclosure](error-disclosure/README.md) | CWE-209 | A02:2025 | handler-unit |
| [Fail open](fail-open/README.md) | CWE-636 | A10:2025 | handler-unit |
| [Open redirect](open-redirect/README.md) | CWE-601 | A01:2025 | handler-unit |
| [Unbounded work](unbounded-work/README.md) | CWE-400 | A06:2025 | executable |
| [Business logic](business-logic/README.md) | CWE-841 | A06:2025 | handler-unit |
| [World readable secret](world-readable-secret/README.md) | CWE-732 | A01:2025 | executable |
| [HTTP response header injection](header-injection/README.md) | CWE-113 | A05:2025 | handler-unit |
| [Symlink following](symlink-following/README.md) | CWE-59 | A01:2025 | executable |
| [Path traversal](path-traversal/README.md) | CWE-22 | A01:2025 | executable |
| [Command injection](command-injection/README.md) | CWE-78 | A05:2025 | executable |
