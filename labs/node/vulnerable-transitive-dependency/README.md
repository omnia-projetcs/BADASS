# Vulnerable transitive dependency

A local settings wrapper introduces lodash.merge 4.6.1 transitively; merging untrusted settings pollutes Object.prototype.

**Technology:** Node.js  
**CWE:** CWE-1395  
**OWASP:** A03:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Upgrade the wrapper dependency from 1.0.0 to 1.0.1, which pins lodash.merge 4.6.2; regenerate the lockfile and verify the resolved transitive version.

## Regression

```sh
make dependency-prepare
make dependency-test
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| empty settings | benign | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} |
| nested preference merge | benign | {"equals": "{\"theme\":\"dark\",\"isAdmin\":false}"} | {"equals": "{\"theme\":\"dark\",\"isAdmin\":false}"} |
| own property is not global authority | benign | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} |
| constructor prototype pollution | attack | {"equals": "{\"theme\":\"light\",\"isAdmin\":true}"} | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} |
| nested constructor prototype pollution | attack | {"equals": "{\"theme\":\"light\",\"isAdmin\":true}"} | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} |
| proto key remains blocked | attack | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} | {"equals": "{\"theme\":\"light\",\"isAdmin\":false}"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

## Dependency evidence

The application imports only a local settings wrapper. That wrapper imports the
real `lodash.merge` package, introducing it transitively. The application source
is identical in both variants. The vulnerable graph is application → wrapper
1.0.0 → `lodash.merge` **4.6.1**; the fixed graph uses wrapper 1.0.1 → **4.6.2**.

Inspect the [vulnerable wrapper manifest](vulnerable/settings-wrapper/package.json),
[vulnerable lockfile](vulnerable/package-lock.json),
[corrected wrapper manifest](fixed/settings-wrapper/package.json) and
[corrected lockfile](fixed/package-lock.json). The wrapper is original local
fixture code, not an affected published package. `--install-links` installs it
as a package instead of a symlink, retaining a reproducible transitive graph.

The library advisory is
[GHSA-h726-x36v-rx45](https://github.com/advisories/GHSA-h726-x36v-rx45).
See [setup, SCA expectations and limitations](../../../docs/DEPENDENCIES.md).

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
