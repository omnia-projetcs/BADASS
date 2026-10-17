# Prototype pollution

Assigning an untrusted __proto__ property changes an object prototype.

| Attribute | Value |
|---|---|
| Technology | TypeScript |
| CWE | CWE-1321 |
| OWASP | A08:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.ts) · [Corrected source](fixed/main.ts)

## Correction

Validate a non-null JSON object, copy into a prototype-free object, and exclude prototype-related keys; preserve legitimate own properties.

## Regression

```sh
python3 tools/lab.py test --case typescript/prototype-pollution --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary property | benign | {"equals": "USER"} | {"equals": "USER"} |
| legitimate own marker remains observable | benign | {"equals": "ADMIN"} | {"equals": "ADMIN"} |
| own false marker shadows prototype data | benign | {"equals": "USER"} | {"equals": "USER"} |
| prototype property | attack | {"equals": "ADMIN"} | {"equals": "USER"} |
| prototype property beside ordinary data | attack | {"equals": "ADMIN"} | {"equals": "USER"} |
| null is not a merge object | robustness | {"equals": "USER"} | {"equals": "DENIED"} |
| array is not a merge object | robustness | {"equals": "USER"} | {"equals": "DENIED"} |
| boolean is not a merge object | robustness | {"equals": "USER"} | {"equals": "DENIED"} |
| string is not a merge object | robustness | {"equals": "USER"} | {"equals": "DENIED"} |
| number is not a merge object | robustness | {"equals": "USER"} | {"equals": "DENIED"} |
| malformed JSON is rejected predictably | robustness | {"stderr_contains": "SyntaxError"} | {"equals": "DENIED"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
