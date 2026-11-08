# Permissive origin regex

A credentialed response handler matches allowed origins using unescaped regex dots. Unrelated domains pass the policy and receive reflected CORS headers plus a synthetic private profile. The response is captured in a real JSON artifact.

| Attribute | Value |
|---|---|
| Technology | Node.js |
| CWE | CWE-625 |
| OWASP | A01:2025 |
| Test scope | `executable` |

[Vulnerable source](vulnerable/main.js) · [Corrected source](fixed/main.js)

## Correction

Use literal DNS separators and a complete match for the narrow approved-origin grammar. Reject controls and malformed inputs before constructing headers. This fixture models handler output for lowercase HTTPS origins with one alphabetic subdomain; browser enforcement, preflight and network delivery are outside scope.

## Regression

```sh
python3 tools/lab.py test --case node/regex-origin --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| approved https://alpha.example.test | benign | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} |
| approved https://beta.example.test | benign | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://beta.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://beta.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://beta.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://beta.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} |
| approved https://research.example.test | benign | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://research.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://research.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://research.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://research.example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} |
| first wildcard separator | attack | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha-example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha-example.test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| second wildcard separator | attack | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example-test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alpha.example-test\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| both wildcard separators | attack | {"equals": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alphaxexampleytest\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}", "files": [{"path": "cors-response.json", "content": "{\"status\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"https://alphaxexampleytest\",\"Access-Control-Allow-Credentials\":\"true\"},\"body\":\"LAB_PRIVATE_PROFILE\"}\n"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| HTTP origin | robustness | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| attacker suffix | robustness | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| userinfo confusion | robustness | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| path outside origin contract | robustness | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| opaque origin | robustness | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":403}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| empty origin | robustness | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| non-string origin | robustness | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| newline suffix | robustness | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} |
| oversized origin | robustness | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} | {"equals": "{\"status\":400}", "files": [{"path": "cors-response.json", "type": "absent"}]} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [MITRE CWE-625](https://cwe.mitre.org/data/definitions/625.html)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
