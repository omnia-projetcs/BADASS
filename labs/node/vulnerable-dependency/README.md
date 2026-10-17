# Vulnerable dependency

A direct dependency on lodash.merge 4.6.1 lets untrusted settings pollute Object.prototype.

**Technology:** Node.js  
**CWE:** CWE-1395  
**OWASP:** A03:2025  
**Test scope:** `executable`

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Upgrade lodash.merge from 4.6.1 to 4.6.2 in the manifest and lockfile, preserving application behavior.

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

The application directly imports `lodash.merge`. Its source is identical in both
variants; the fix upgrades the package from **4.6.1 to 4.6.2** in the
[manifest](fixed/package.json) and [lockfile](fixed/package-lock.json).
The [vulnerable manifest](vulnerable/package.json) and
[vulnerable lockfile](vulnerable/package-lock.json) retain the affected version.

[GHSA-h726-x36v-rx45](https://github.com/advisories/GHSA-h726-x36v-rx45)
documents the prototype pollution flaw. CWE-1395 describes the application-level
dependency issue; the library flaw is CWE-1321. See
[setup, SCA expectations and limitations](../../../docs/DEPENDENCIES.md).

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
