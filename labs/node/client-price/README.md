# Client-controlled price

Checkout trusts the unit price sent by a client product selector instead of the server catalog. A caller changes a nominally read-only field and obtains an underpriced order receipt. Quantities and amounts use bounded integer currency units.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-602 |
| OWASP | A06:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Recompute unit price and total from the trusted product catalog, validate quantity and available balance, and persist only the authoritative receipt. Treat the client quote as informational. The fixture writes a real local receipt but does not charge a payment provider or implement a persistent multi-order wallet.

## Regression

```sh
python3 tools/lab.py test --case node/client-price --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| book purchase | benign | {"equals": "{\"status\":201,\"total\":120,\"remaining\":880}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":120,\"total\":120,\"remaining\":880}\n"}]} | {"equals": "{\"status\":201,\"total\":120,\"remaining\":880}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":120,\"total\":120,\"remaining\":880}\n"}]} |
| multiple books | benign | {"equals": "{\"status\":201,\"total\":360,\"remaining\":640}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":3,\"unit_price\":120,\"total\":360,\"remaining\":640}\n"}]} | {"equals": "{\"status\":201,\"total\":360,\"remaining\":640}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":3,\"unit_price\":120,\"total\":360,\"remaining\":640}\n"}]} |
| lamp purchase | benign | {"equals": "{\"status\":201,\"total\":250,\"remaining\":750}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":1,\"unit_price\":250,\"total\":250,\"remaining\":750}\n"}]} | {"equals": "{\"status\":201,\"total\":250,\"remaining\":750}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":1,\"unit_price\":250,\"total\":250,\"remaining\":750}\n"}]} |
| exact balance | benign | {"equals": "{\"status\":201,\"total\":1000,\"remaining\":0}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":4,\"unit_price\":250,\"total\":1000,\"remaining\":0}\n"}]} | {"equals": "{\"status\":201,\"total\":1000,\"remaining\":0}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":4,\"unit_price\":250,\"total\":1000,\"remaining\":0}\n"}]} |
| free book | attack | {"equals": "{\"status\":201,\"total\":0,\"remaining\":1000}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":0,\"total\":0,\"remaining\":1000}\n"}]} | {"equals": "{\"status\":201,\"total\":120,\"remaining\":880}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":120,\"total\":120,\"remaining\":880}\n"}]} |
| underpriced lamp | attack | {"equals": "{\"status\":201,\"total\":1,\"remaining\":999}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":1,\"unit_price\":1,\"total\":1,\"remaining\":999}\n"}]} | {"equals": "{\"status\":201,\"total\":250,\"remaining\":750}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":1,\"unit_price\":250,\"total\":250,\"remaining\":750}\n"}]} |
| multiple underpriced lamps | attack | {"equals": "{\"status\":201,\"total\":3,\"remaining\":997}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":3,\"unit_price\":1,\"total\":3,\"remaining\":997}\n"}]} | {"equals": "{\"status\":201,\"total\":750,\"remaining\":250}", "files": [{"path": "order.json", "content": "{\"product\":\"lamp\",\"quantity\":3,\"unit_price\":250,\"total\":750,\"remaining\":250}\n"}]} |
| client overstates price | functional | {"equals": "{\"status\":201,\"total\":900,\"remaining\":100}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":900,\"total\":900,\"remaining\":100}\n"}]} | {"equals": "{\"status\":201,\"total\":120,\"remaining\":880}", "files": [{"path": "order.json", "content": "{\"product\":\"book\",\"quantity\":1,\"unit_price\":120,\"total\":120,\"remaining\":880}\n"}]} |
| insufficient balance | benign | {"equals": "{\"status\":402}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":402}", "files": [{"path": "order.json", "type": "absent"}]} |
| boolean quantity | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| negative quantity | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| fractional quantity | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| boolean price | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| negative price | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| missing price | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| unknown product | robustness | {"equals": "{\"status\":404}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":404}", "files": [{"path": "order.json", "type": "absent"}]} |
| prototype property name | robustness | {"equals": "{\"status\":404}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":404}", "files": [{"path": "order.json", "type": "absent"}]} |
| non-object request | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |
| non-string product | robustness | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "order.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-602 — Client-Side Enforcement of Server-Side Security](https://cwe.mitre.org/data/definitions/602.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
