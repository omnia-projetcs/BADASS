# Benchmark methodology

Each entry in `catalog/cases.json` describes one target weakness, a vulnerable
source file, a corrected source file, the remediation contract, and paired test
vectors. The same input reaches both versions. Benign inputs must retain the same
observable behavior. Attack inputs must demonstrate the weakness in the vulnerable
version and satisfy the corrected contract in the fixed version.

`executable` examples perform actual operations in a temporary working directory.
`handler-unit`, `state-machine-unit`, and `configuration-unit` examples validate an
application boundary without claiming to reproduce a complete deployment.
`loopback-integration` exercises an actual local HTTP request. `ai-boundary-unit`
validates application controls around a model; it does not run a model.

The CLI examples isolate small data flows for auditing. They are not full web apps.
For example, XSS fixtures generate an HTML body but do not launch a browser, and
API examples mostly test handler logic rather than authentication middleware.

## Running and repairing cases

```sh
python3 tools/lab.py list --language java
python3 tools/lab.py test --case java/xxe --strict
python3 tools/lab.py test --language python --strict
python3 tools/lab.py test --cwe CWE-89 --strict
python3 tools/lab.py test --strict --output reports/regression.json
```

To evaluate a repair, place the candidate repair in the case's `fixed/` source,
then rerun the case. Preserve the trusted catalog and test oracles outside the
agent's editable input. Do not let a repair agent rewrite its own expected results.
Passing these vectors establishes only the stated contract; review additional
inputs, deployment assumptions, and new attack surfaces before accepting a patch.

The runner gives each variant and vector a fresh working directory with synthetic
files. It compiles native fixtures, enforces timeouts, and records exit codes and
failed output. C/C++ memory faults must produce the expected sanitizer diagnostic;
an unrelated crash is not a passing result. A missing runtime is `skip`, not `pass`.
Use `--strict` to make missing runtimes fail the run. Compile failures and sandbox
restrictions are failures, not successful mitigations.

## Detection scoring

Normalize scanner output into this JSON format:

```json
[
  {"case_id": "python/sql-injection", "variant": "vulnerable", "cwe": "CWE-89"},
  {"case_id": "python/sql-injection", "variant": "fixed", "cwe": "CWE-89"}
]
```

```sh
python3 tools/lab.py score --findings findings.json --output reports/score.json
```

The first example is a true positive and the second is a false positive for the
declared target. Scoring deduplicates exact findings and reports precision, recall,
misses, and unknown case identifiers. Metrics are computed on `(case_id, CWE)`
pairs. The scorer does not guess CWE equivalences or infer a vulnerability from
an arbitrary scanner rule name. Exporting SARIF or vendor formats requires an
explicit normalization step using file paths and documented rule-to-CWE mappings.

Fixed examples are negative controls only for the declared target weakness under
the documented assumptions. Other scanner findings need manual triage; the corpus
does not assert that every line is production hardened.

SQL injection is implemented in every technology section with real SQLite
queries, filter-bypass and UNION vectors, and parameter-bound corrections. See
[SQL injection coverage and driver prerequisites](SQL-INJECTION.md). These cases
do not simulate a database by printing SQL or searching for known payload strings.

Keep `fixed/`, the catalog, README files and test expectations out of blind scanner
or agent input. Otherwise labels and corrections leak the answer. For normal SAST,
scan the intended source directories and use the catalog only for scoring.

## Coverage semantics

The exhaustive matrix enumerates every entry in the imported MITRE snapshot,
including deprecated entries. It distinguishes actual weaknesses from categories
and views. `implemented` means a code pair and vectors exist; test execution status
comes from a regression report. `gap` means no direct case exists. `taxonomy-only`
means the entry is a category or view rather than an executable weakness.

The [technology matrix](TECHNOLOGY-MATRIX.md) crosses every weakness with all
14 sections. A case only fills its exact CWE and technology cell. The
[coverage plan](../catalog/coverage-plan.json) defines a shared 16-family baseline
and eight additional C/C++ targets. Within that plan, an absent case is `gap`.
Outside it, an absent case is `unassessed`: applicability needs review, and the
weakness must not be counted as covered or dismissed as not applicable. There is
no defensible single count of all possible vulnerabilities for a language without
specifying frameworks, native boundaries, configuration and deployment context.

The CLI coverage JSON includes `by_technology` with case links, target flags,
per-section totals and all weakness rows. Filters restrict the evidence used:
`coverage --language java` leaves other sections without implementation evidence
in that filtered report. Categories and views remain in the global `cwe` array.

The common baseline includes SQL, command, HTML, log and HTTP-header injection;
path traversal and symbolic-link following; object-level and function-level
authorization; hardcoded credentials; error disclosure; fail-open decisions;
open redirects; unbounded work; business logic; and file permissions. Context
sections exercise these at handler or tool boundaries without running a web
server or LLM. Native C/C++ cases additionally cover stack and heap overflow,
out-of-bounds reads, use-after-free, double free, null dereferences, format strings
and integer wraparound. Arithmetic wraparound is observed through the calculated
result; unsigned wraparound is defined behavior and does not require a sanitizer.

The symbolic-link cases create a real preplaced link and observe whether writing
through it changes the synthetic secret. Exclusive creation protects the final
path component in a trusted parent directory. This is not protection against
attacker-controlled ancestor directories. Permission tests inspect actual POSIX
mode bits, not ACLs, Windows permissions or the process umask. Resource tests use
small allocations to exercise a limit without exhausting the machine.

Further work includes framework-specific authentication and session handling,
serialization, XML parsers, uploads, cryptographic APIs, concurrency and unsafe
native interfaces in additional languages. An existing example in one section
does not discharge this work for other sections.

Mappings to OWASP are project-maintained topical mappings. They are not official
MITRE mapping claims or a certification. The scope includes Web Top 10:2025,
API Security Top 10:2023 and LLM Top 10:2025. ASVS, WSTG, MASVS, hardware verification,
cloud configuration and other OWASP projects are not fully implemented here.
One representative case per category does not cover every risk within that category.

## Isolation and prerequisites

Use `make container-build container-test` for the full suite on Linux with Docker.
The image build downloads packages. Test execution has no external network, no
published ports, a read-only source mount, an unprivileged runtime user, dropped
capabilities and explicit memory/process limits. Only `reports/` is a writable
host mount. Temporary fixture data stays in the container.

To run a single section in the same container, use
`make container-test LAB_ARGS='test --language dotnet --strict'`.
The runner supplies an owned `XDG_RUNTIME_DIR` for .NET named mutexes when the host
UID has no container account; see the upstream
[.NET runtime discussion](https://github.com/dotnet/runtime/issues/135726).

The fixture runner itself is not a security sandbox. Native execution inherits
the caller's permissions; use it only with reviewed fixtures and synthetic data.
Command examples target POSIX `/bin/sh` and `/usr/bin/printf`. Directory fixtures
assume `public/` is controlled by the server. The allowlisted filename is not a
general-purpose solution for attacker-writable directory trees or symlink races.

The container pins TypeScript to 5.6.3 but uses a moving .NET 8 SDK tag and Debian
package repositories. Record the built image digest and tool versions for a
repeatable benchmark campaign; this is not a bit-for-bit reproducible build.
