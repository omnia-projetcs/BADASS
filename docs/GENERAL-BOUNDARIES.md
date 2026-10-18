# General execution and data boundaries

These six Python cases cover command-option parsing, format-string disclosure,
filesystem races, JSON parser disagreement, Unicode normalization and password
recovery replay. Each has an executable
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

## Run

From the repository root:

```sh
python3 tools/lab.py test --case python/argument-injection --strict
python3 tools/lab.py test --case python/format-string-disclosure --strict
python3 tools/lab.py test --case python/file-create-race --strict
python3 tools/lab.py test --case python/json-parser-conflict --strict
python3 tools/lab.py test --case python/unicode-path-validation --strict
python3 tools/lab.py test --case python/password-reset-replay --strict
python3 -m unittest discover -s tests -p test_general_boundaries.py -v
python3 -m unittest discover -s tests -p test_parser_recovery_boundaries.py -v
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
