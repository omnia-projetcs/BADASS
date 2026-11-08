# Vulnerable direct and transitive dependencies

These cases cover [CWE-1395](https://cwe.mitre.org/data/definitions/1395.html),
Dependency on Vulnerable Third-Party Component, mapped by this project to
OWASP Web Top 10:2025 A03 (Software Supply Chain Failures).

The underlying flaw is prototype pollution (CWE-1321) in `lodash.merge`:
[GHSA-h726-x36v-rx45](https://github.com/advisories/GHSA-h726-x36v-rx45)
lists versions before 4.6.2 as affected and 4.6.2 as patched. The fixtures pin
4.6.1 and 4.6.2 respectively. The advisory has no assigned CVE; its GHSA identifier
is the reference. These historical pins are controls for this advisory, not a
recommendation of a current package version or a guarantee against other flaws.

| Case | Vulnerable dependency graph | Corrected dependency graph |
|---|---|---|
| [Direct](../labs/node/vulnerable-dependency/README.md) | application → lodash.merge 4.6.1 | application → lodash.merge 4.6.2 |
| [Transitive](../labs/node/vulnerable-transitive-dependency/README.md) | application → local settings wrapper 1.0.0 → lodash.merge 4.6.1 | application → local settings wrapper 1.0.1 → lodash.merge 4.6.2 |

The wrapper is a local first-party npm fixture, not a vulnerable published product.
It imports and calls the real third-party library. The application declares only
the wrapper in the transitive case; npm's lockfile records the library beneath it.
Physical hoisting into `node_modules` does not make that dependency direct.

## Reproduce

From the repository root, with Node.js 18+ and npm 9+ installed:

```sh
make dependency-prepare
make dependency-test
```

Preparation uses `npm ci`, committed lockfiles and registry integrity hashes.
It disables lifecycle scripts and automatic audit requests. The local wrapper is
installed as a package using `--install-links`, with the same option during install
and clean reinstall. A cold cache needs registry access; dependencies are not
committed to Git. Runtime checks then need no network.

The standalone command is `node labs/node/dependency-regression.cjs`. It checks
both variants against the vectors in `catalog/cases.json`, launches a fresh process
per vector, enforces a timeout and rejects crashes or missing packages. The two
application files in each pair must be identical. The only functional correction
is the dependency update and corresponding lockfile change.

There are six vectors per case, run against both variants (24 checks total):

- Empty settings and a nested theme preference preserve normal merge behavior.
- A user-owned `isAdmin` property must not grant privileges to unrelated objects.
- Top-level and nested `constructor.prototype` payloads demonstrate global pollution
  in the vulnerable version; the fixed version leaves other objects unchanged.
- A `__proto__` payload stays blocked in both pinned versions, guarding against
  accidentally treating every prototype-related input as an exploit.

The general `tools/lab.py` runner and documentation generator were removed before
these cases were added. The standalone targets work without those files. Existing
general runner commands elsewhere in the repository are not the execution path
for these dependency tests. The default Docker image does not preload these new
npm packages; prepare them before running the checks in an offline environment.

## Scanner evaluation

Scan each `vulnerable/` or `fixed/` directory separately, including `package.json`,
`package-lock.json` and `settings-wrapper/` where present. Exclude counterpart
variants, case documentation, the catalog and expected outputs from blind scans.

For SCA, expect the advisory on `lodash.merge` 4.6.1 and no finding for that same
advisory on 4.6.2. Record package name, resolved version, advisory identifier,
dependency relationship and the manifest/lockfile evidence. For the transitive
case, retain the full application → wrapper → library path. Scanning only root
manifest names would miss it. A source-only SAST scan need not identify this flaw.

The catalog uses CWE-1395 for the application's dependency problem and records
CWE-1321 separately as `dependency.underlying_cwe`. Normalize scanner findings
explicitly to the target case and CWE; do not silently equate the two weaknesses.
Do not treat unrelated advisories on the fixed variant as false positives.

Version evidence establishes exposure to a known advisory. The regression supplies
separate evidence that the affected operation is reachable in this application.
These examples cover npm only; other ecosystems, vendored libraries, OS packages,
containers, unsupported components (CWE-1104), malicious packages and artifact
integrity need their own cases. They do not gain coverage from this mapping.
