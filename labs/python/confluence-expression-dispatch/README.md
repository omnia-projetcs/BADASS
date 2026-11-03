# Confluence: pre-auth expression evaluation

An original Confluence-inspired pre-authentication expression-dispatch model evaluates path expressions while preparing a redirect. A restricted AST interpreter can set a response header to synthetic private state. The model demonstrates an evaluated-request boundary; it is not an OGNL engine, Java runtime, shell or complete Confluence RCE reproduction.

| Attribute | Value |
|---|---|
| Technology | Python |
| CWE | CWE-917 |
| CVE | CVE-2022-26134 |
| OWASP | A05:2025 |
| Test scope | `handler-model` |

[Vulnerable source](vulnerable/main.py) · [Corrected source](fixed/main.py)

## Correction

Treat the request path as data and percent-encode it when constructing the login redirect, without invoking an expression interpreter. The miniature vulnerable grammar exposes only setHeader with string or synthetic-secret arguments; it cannot load classes or execute system commands. Authentication later in dispatch does not protect earlier expression evaluation. Actual remediation requires a patched Confluence product.

## Regression

```sh
python3 tools/lab.py test --case python/confluence-expression-dispatch --strict
```

Run from the repository root. Exact inputs and expected outputs are in
[the catalog](../../../catalog/cases.json). Both variants are tested.

The runner also checks every declared file effect. `functional` vectors can specify a useful
operation that the vulnerable implementation did not support correctly; `robustness` vectors
exercise malformed inputs. `benign` vectors require identical expectations.

| Vector | Type | Vulnerable expectation | Fixed expectation |
|---|---|---|---|
| ordinary page redirect | benign | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fpage"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fpage"}}} |
| encoded ordinary path | benign | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fpage"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fpage"}}} |
| unicode ordinary path | benign | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fcaf%C3%A9"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2Fwiki%2Fcaf%C3%A9"}}} |
| expression leaks private state before login | attack | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20secret%29%7D%2F", "X-Lab": "LAB_CONFLUENCE_PRIVATE"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20secret%29%7D%2F"}}} |
| encoded expression before login | attack | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20secret%29%7D%2F", "X-Lab": "LAB_CONFLUENCE_PRIVATE"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20secret%29%7D%2F"}}} |
| expression creates attacker header | attack | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20%22CHANGED%22%29%7D%2F", "X-Lab": "CHANGED"}}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7BsetHeader%28%22X-Lab%22%2C%20%22CHANGED%22%29%7D%2F"}}} |
| unsupported expression stays data | functional | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 302, "headers": {"Location": "/login?next=%2F%24%7Bunknown%28%29%7D%2F"}}} |
| wrong input type | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |
| invalid UTF8 | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |
| newline path | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |
| oversized path | robustness | {"equals": {"status": 400, "error": "invalid path"}} | {"equals": {"status": 400, "error": "invalid path"}} |

## Inspiration and provenance

Original benchmark implementation inspired by the documented weakness;
no third-party exploit source is copied or executed.

- [Atlassian Confluence CVE-2022-26134 — official advisory](https://confluence.atlassian.com/doc/confluence-security-advisory-2022-06-02-1130377146.html)
- [EDB-50952 — Confluence Data Center expression injection](https://www.exploit-db.com/exploits/50952)

This example demonstrates the declared weakness within the documented fixture assumptions.
It is not a production application or a proof that every related attack is prevented.

[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)
