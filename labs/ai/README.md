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
