# General execution and data boundaries

These three Python cases add command-option parsing, format-string disclosure
and filesystem races to the general vulnerability corpus. Each has an executable
vulnerable counterpart, a correction and catalog vectors. They require only the
Python standard library on the project's Linux environment.

| Case | Observed defect | Correction |
|---|---|---|
| [Argument injection](../labs/python/argument-injection/README.md) — CWE-88 | A real child process interprets an input query as its internal private-record option even with `shell=False`. | Insert the child parser's `--` option terminator before user data. |
| [Format-string disclosure](../labs/python/format-string-disclosure/README.md) — CWE-134 | A replacement field traverses the profile object's private dictionary. | Accept only public `name` and `team` placeholders and supply only those strings. |
| [File creation race](../labs/python/file-create-race/README.md) — CWE-367 | An attacker inserts a symlink after an existence check and before opening the output file. | Use atomic exclusive creation and treat an intervening file or link as a conflict. |

## Run

From the repository root:

```sh
python3 tools/lab.py test --case python/argument-injection --strict
python3 tools/lab.py test --case python/format-string-disclosure --strict
python3 tools/lab.py test --case python/file-create-race --strict
python3 -m unittest discover -s tests -p test_general_boundaries.py -v
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

The argument pattern is inspired by
[EDB-44993](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/remote/44993.rb).
The symlink-write pattern is inspired by
[EDB-24749](https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/linux/local/24749.sh);
the deterministic race schedule is an original extension. No third-party exploit
source or affected application is included.
