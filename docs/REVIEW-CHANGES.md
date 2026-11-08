# Review implementation notes

Base: `87f8d5f162a1970becc2909211fabcca8165386d`.
Implementation and local verification: 2026-10-17.
See the [French application guide](../GUIDE_CORRECTIONS_FR.md) for application
commands, detailed changes and the delivered evidence.

## Changes

The deleted tooling was restored from parent commit
`80f447c1be08de70042cf9fc6387a98b01dc6d72`, then extended with independent
observations of file effects, operation-level repair oracles, explicit exit
contracts, synthetic environment configuration and a nonempty smoke gate.

The source corrections address Go/.NET secret classification, strict C/C++
numeric conversion, Python token and session lifecycles, real salted password
records, validated Unicode/type handling, Node/TypeScript object shape handling,
and acceptance of independently verified security repairs. Positive functional
vectors preserve useful work and prevent deny-everything repairs from passing.

Eight pairs were added: SQL ORDER BY identifiers, second-order SQL injection,
HTML attribute XSS, REST tenant authorization, order workflow, concurrent order
shipment, SSRF redirects, and AI tool argument capabilities. Negative quantity
cases were remapped from CWE-841 to CWE-1284; a stateful workflow represents CWE-841
separately. The catalog has 280 pairs, 1,075 vectors and 52 distinct CWE mappings.

`tools/export_blind.py` creates opaque source paths and a private mapping outside
the corpus, then normalizes scanner path/CWE findings for the existing scorer.
It preserves source bytes and does not claim to remove all source-level clues or
training contamination. The CI file provides tooling, smoke and strict Docker
jobs, with read-only repository permissions and a pinned checkout action.

## Local verification and explicit gaps

- Catalog validation: 280 valid pairs.
- Tooling tests: 101 discovered, 100 passed, one TypeScript compiler test skipped.
- Required smoke gate: six pairs, 102 passed checks.
- Whole-catalog local attempt: 162 pairs passed, 115 skipped for missing runtimes,
  and three failed because their SQLite development dependencies are absent.
- The attempt executed 1,338 variant checks: 1,324 passed, and 14 Node SQL checks
  failed while loading the missing `sqlite3` module. The C/C++ SQL pairs failed
  to compile because `sqlite3.h` is absent, so their vectors did not execute.
- All eight newly added pairs pass in that whole-catalog attempt.

The skipped language sections are TypeScript, PHP, Ruby, Go, Java, Rust and .NET.
The Go and .NET source changes are reviewed and have regression vectors, but have
not been compiled or executed in this environment. The full Docker regression
and remote GitHub Actions workflow have not run here. Do not describe this local
attempt as a complete green run across all 14 sections.

The ZIP includes original reports under `reports/`, which is ignored by Git and
therefore not included in the source patch. Reports preserve failures and skips;
they contain source/vector digests and are accompanied by a delivery summary.

## Fixture boundaries

Both vulnerable and fixed variants remain executable benchmark controls.
The runner is not an adversarial process sandbox. File permissions are POSIX
mode checks, cryptographic cost is a bounded fixture profile, concurrency is
local SQLite transaction behavior, and SSRF uses an isolated loopback server.
AI evidence and tool-capability tests exercise application controls without
running a model. Read [the methodology](BENCHMARK.md) before extending these
results to a deployment or evaluating externally supplied candidate code.
