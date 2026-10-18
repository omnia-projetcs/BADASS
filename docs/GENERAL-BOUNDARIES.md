# General execution and data boundaries

These nine Python cases cover command-option parsing, format-string disclosure,
filesystem races, JSON parser disagreement, Unicode normalization and password
recovery replay, webhook signatures, decompression amplification and session expiry.
Each has an executable
vulnerable counterpart, a correction and catalog vectors. They require only the
Python standard library on the project's Linux environment.

| Case | Observed defect | Correction |
|---|---|---|
| [Argument injection](../labs/python/argument-injection/README.md) — CWE-88 | A real child process interprets an input query as its internal private-record option even with `shell=False`. | Insert the child parser's `--` option terminator before user data. |
| [Format-string disclosure](../labs/python/format-string-disclosure/README.md) — CWE-134 | A replacement field traverses the profile object's private dictionary. | Accept only public `name` and `team` placeholders and supply only those strings. |
| [File creation race](../labs/python/file-create-race/README.md) — CWE-367 | An attacker inserts a symlink after an existence check and before opening the output file. | Use atomic exclusive creation and treat an intervening file or link as a conflict. |
| [JSON parser conflict](../labs/python/json-parser-conflict/README.md) — CWE-436 | A gateway checks the first amount, but a worker debits the last duplicate amount. | Reject duplicate keys and pass the validated object to execution. |
| [Unicode path validation](../labs/python/unicode-path-validation/README.md) — CWE-180 | NFKC normalization turns compatible characters into path traversal after the filename check. | Normalize before validation and read the exact resolved, confined path. |
| [Password-reset replay](../labs/python/password-reset-replay/README.md) — CWE-640 | The same expiring reset token replaces the password multiple times. | Consume the token atomically with the password update. |
| [Webhook signature](../labs/python/webhook-signature/README.md) — CWE-347 | The HMAC comparison result is ignored, allowing an unauthenticated invoice update. | Require a matching signature over the raw body before parsing and writing. |
| [Decompression amplification](../labs/python/decompression-amplification/README.md) — CWE-409 | Bounded compressed input expands beyond the output budget. | Bound the decoder output and publish only complete, accepted data. |
| [Session expiration](../labs/python/session-expiration/README.md) — CWE-613 | Stored expiry and revocation flags are ignored when reading private data. | Enforce both checks for every authenticated operation. |

## Run

From the repository root:

```sh
python3 tools/lab.py test --case python/argument-injection --strict
python3 tools/lab.py test --case python/format-string-disclosure --strict
python3 tools/lab.py test --case python/file-create-race --strict
python3 tools/lab.py test --case python/json-parser-conflict --strict
python3 tools/lab.py test --case python/unicode-path-validation --strict
python3 tools/lab.py test --case python/password-reset-replay --strict
python3 tools/lab.py test --case python/webhook-signature --strict
python3 tools/lab.py test --case python/decompression-amplification --strict
python3 tools/lab.py test --case python/session-expiration --strict
python3 -m unittest discover -s tests -p test_general_boundaries.py -v
python3 -m unittest discover -s tests -p test_parser_recovery_boundaries.py -v
python3 -m unittest discover -s tests -p test_delivery_session_boundaries.py -v
```

## Evidence and limits

The argument case starts the same fixture file in its internal worker mode as a
separate process. No shell or external service is used. The internal search tool
has a private-record flag so the change in argument interpretation is visible.
The repaired wrapper preserves ordinary queries and treats option-looking text
as a literal search. Other child programs require their own option contract.

The formatter is Python's actual `str.format`, with attribute and item traversal.
Tests change the profile's private value and observe its disclosure. The fixed
renderer preserves public values, literal braces and Unicode, while rejecting
unsupported traversal, conversions and format specifications. This is not a
Jinja/Twig exploit, HTML escaping test or demonstration of arbitrary execution.

The race case uses events to schedule a real attacker thread in the check/use
window. Tests inspect the symlink and victim bytes; truncation is tested as well
as replacement. An additional two-writer test places both writers past the check
before either opens the file, verifying that exclusive creation admits only one.
The parent directory is trusted and all files belong to the local fixture.

The JSON case parses the raw input twice with different duplicate-key policies.
The gateway caps payments at 100 units; the downstream worker accepts larger
integer amounts and commits a real SQLite debit and ledger row. Tests inspect
both rows and the generated snapshot. Escaped duplicate keys are decoded before
comparison. The fixed path rejects ambiguous keys and executes the checked object.
This is an in-process gateway/worker model, not an HTTP request-smuggling server.

The Unicode reader explicitly applies NFKC as an application choice; the case
does not assume that the operating system normalizes filenames. Tests replace
private file contents and verify the bytes actually returned by the vulnerable
reader. The correction preserves compatible public names and rejects symlinks
that resolve outside the public root. That root is trusted and stable; concurrent
changes to directories or links are outside this case.

The recovery case creates a random token for each run and stores its hash, an
expiry and a consumption flag in SQLite. It verifies real salted PBKDF2 password
hashes after every scenario. The fixture's token selectors and clock values are
test controls, and the returned credential observations are not public API data.
Unit tests also race two separate database connections and inject a password-write
failure to check that consumption and password replacement commit or roll back
together. Email delivery, session revocation and production password policy are
outside scope. No reset message is sent.

The webhook case computes a real HMAC-SHA256 but discards the comparison result
in the vulnerable handler. Tests sign one body and submit another, inspect the
invoice rows, and verify that the fixed handler rejects the request before JSON
parsing. Valid signatures include the exact whitespace and escaped field names.
Keys and signatures are generated by the local harness. No webhook endpoint is
opened; duplicate-delivery protection is outside this case.

The zlib importer accepts at most 1024 compressed bytes and is intended to allow
at most 1024 expanded bytes. Catalog attacks expand to at most 4096 bytes; a unit
test uses 16384 bytes and observes that the fixed decoder produces only 1025 bytes
before rejecting. File observations verify both accepted content and absence on
rejection. Truncated, concatenated and trailing-data streams are rejected in both
variants. This case does not measure CPU exhaustion or nested archive handling.

The session case stores random token hashes, expiry and revocation in SQLite.
Tests commit a logout, close the connection, reopen it and check both the stored
revocation and access to a changed private report. The fixed handler also rejects
at the exact expiry boundary before querying that report. Clock values belong
to the harness, not the caller of a real service. Concurrent in-flight requests,
cookie transport, idle timeouts and session renewal are outside scope.

The argument pattern is inspired by
[EDB-44993](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/remote/44993.rb).
The symlink-write pattern is inspired by
[EDB-24749](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/linux/local/24749.sh);
the deterministic race schedule is an original extension. No third-party exploit
source or affected application is included.

The JSON, Unicode and recovery cases are original general examples, documented
against [Python JSON parsing](https://docs.python.org/3/library/json.html#repeated-names-within-an-object),
[Python normalization](https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize)
and the [OWASP recovery guidance](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
They are not attributed to a specific Exploit-DB entry.

The additional delivery and session examples reference
[webhook signature verification](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries),
[zlib output limits](https://docs.python.org/3/library/zlib.html#decompression-objects)
and [CWE-613](https://cwe.mitre.org/data/definitions/613.html).
They are also original general fixtures without a specific Exploit-DB attribution.
