# Review implementation notes

Implementation and verification: 2026-11-12.
See the [French application guide](../GUIDE_CORRECTIONS_FR.md) for application
commands, detailed changes and verification evidence.

## Changes

The benchmark tooling includes independent observations of file effects,
operation-level repair oracles, explicit exit contracts, synthetic environment
configuration, a nonempty smoke gate, and a deterministic training dataset exporter
(`tools/export_training.py`).

Comprehensive cross-language and full-stack audit fixes cover all 14 technology
sections (`c`, `cpp`, `go`, `php`, `rest-api`, `node`, `python`, `cgi`, `dotnet`,
`typescript`, `java`, `ruby`, `rust`, `ai`) and the three multi-file application
projects (`projects/django-jsonfield`, `projects/nextjs-middleware`,
`projects/tenant-billing`):

- **Deduplication and contextualization of training records**: Distinct module
  docstrings and contextual headers across `python`, `cgi`, `rest-api`, `ai`, `c`
  and `cpp` eliminate all duplicate training conversations in
  `enrichissement/vulnerabilities.training.jsonl` (`1,023` unique records across
  `341` cases, `duplicates_removed: 0`).
- **Constant-time credential comparison (CWE-798)**: All 14 `hardcoded-credentials`
  fixed variants compare secrets in constant time (`hmac.compare_digest`,
  `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`,
  `CryptographicOperations.FixedTimeEquals`, `MessageDigest.isEqual`,
  `hash_equals`, `OpenSSL.fixed_length_secure_compare`, and custom
  `constant_time_equals` in C, C++ and Rust).
- **Atomic owner-only file permissions (CWE-732) and symlink protection (CWE-59)**:
  All `world-readable-secret` fixed variants apply `0600` permissions at creation
  or directly on the open file descriptor/handle before closing, eliminating
  path-based TOCTOU windows. `symlink-following` fixed variants combine
  `O_CREAT | O_EXCL` with `O_NOFOLLOW` where available and preserve close errors.
- **Header and log injection hardening (CWE-113, CWE-117)**: All 14
  `header-injection` fixed variants reject `\r`, `\n`, and null/control bytes.
  `log-injection` fixed variants escape `\` prior to `\r` and `\n` to prevent
  forged escape sequences.
- **Prototype pollution (CWE-1321)**: `node/prototype-pollution` and
  `typescript/prototype-pollution` vulnerable variants use recursive object merging
  so `__proto__` and `constructor.prototype` payloads genuinely pollute
  `Object.prototype`, while fixed variants validate object shapes and copy only
  safe own keys into a prototype-free object.
- **Strict numeric bounds and error handling (CWE-190, CWE-400, CWE-1284)**:
  `unbounded-work`, `business-logic`, `out-of-bounds-read`, and `integer-overflow`
  across C, C++, Rust, Go, Node.js, TypeScript, PHP, Ruby, Java, .NET and Python
  enforce strict integer parsing and bounds before allocation or state mutation,
  returning `"DENIED"` cleanly on malformed inputs without unhandled exceptions or
  signed UB.
- **Idiomatic C++ native memory models**: `labs/cpp/*` memory-safety fixtures use
  C++ allocations (`new[]`/`delete[]`), `<cstdio>`, `<cstdlib>`, `<cstring>`, and
  `std::string`.
- **Full-stack projects (`projects/*`)**:
  - `projects/django-jsonfield`: pinned `requirements.lock` to patched Django
    `5.1.14` and restricted JSON filter key characters.
  - `projects/nextjs-middleware`: pinned `package.json` to patched Next.js
    `14.2.25`, added defense-in-depth authorization in `pages/api/private/invoices.js`,
    and removed unused imports.
  - `projects/tenant-billing`: added the missing vulnerable migration, enforced
    constant-time HMAC verification (`hmac.compare_digest`), prevented symlinks and
    path traversal in exports, enforced atomic single-use invitations with
    `select_for_update()`, and hardened view payload parsing.

The catalog has **395 case pairs**, **1,999 regression vectors** (**3,998 declared
variant checks**), and **102 distinct CWE mappings** across **14 technology
sections** and **30 OWASP categories**.

`tools/export_blind.py` creates opaque source paths and a private mapping outside
the corpus, then normalizes scanner path/CWE findings for the existing scorer.
It preserves source bytes and does not claim to remove all source-level clues or
training contamination.

## Verification summary

- Catalog validation (`python3 tools/lab.py validate`): **395 valid pairs**.
- Documentation freshness (`python3 tools/render_docs.py --check`): **current**.
- Training export freshness (`python3 tools/export_training.py --check`):
  **395 cases, 1,185 examples, 0 duplicates removed, status `current`**.
- Tooling and boundary unit tests (`python3 -m unittest discover -s tests -v`):
  **214 tests discovered and passing** (33 skipped when optional native/external
  compilers are absent on the host).
- Python, CGI, REST API, and AI strict regressions
  (`python3 tools/lab.py test --language {python,cgi,rest-api,ai} --strict`):
  **all 161 Python-executed case pairs pass**.

## Fixture boundaries

Both vulnerable and fixed variants remain executable benchmark controls.
The runner is not an adversarial process sandbox. File permissions are POSIX
mode checks, cryptographic cost is a bounded fixture profile, concurrency is
local SQLite transaction behavior, and SSRF uses an isolated loopback server.
AI evidence and tool-capability tests exercise application controls without
running a model. Read [the methodology](BENCHMARK.md) before extending these
results to a deployment or evaluating externally supplied candidate code.
