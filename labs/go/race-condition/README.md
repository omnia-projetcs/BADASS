# Race condition

Concurrent goroutines check the same account balance without a mutex, allowing multiple 80-unit withdrawals from a 100-unit balance.

| Attribute | Value |
|---|---|
| Technology | Go |
| CWE | CWE-362 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.go) · [Corrected source](fixed/main.go)

## Correction

Guard the balance check and deduction together inside a critical section protected by sync.Mutex.

## Regression

```sh
python3 tools/lab.py test --case go/race-condition --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| single withdrawal | benign | {"equals": "WITHDRAWN:80"} | {"equals": "WITHDRAWN:80"} |
| concurrent double withdrawal | attack | {"equals": "WITHDRAWN:160"} | {"equals": "WITHDRAWN:80"} |

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
