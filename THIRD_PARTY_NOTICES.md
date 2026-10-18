# Third-party notices

Original project code is covered by [LICENSE](LICENSE).

## Exploit-DB references

The Exploit-DB-inspired Python cases are original educational implementations
inspired by these public reports:

- Dawid Morawski, Online Food Delivery 2.04 authentication bypass, EDB-41029:
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/41029.txt
- John Page (hyp3rlinx), eXtplorer 2.1.9 ZIP directory traversal, EDB-39816,
  CVE-2016-4313:
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/39816.php
- Iam Alvarez, mailcow Host Header Password Reset Poisoning, EDB-52485,
  CVE-2025-25198 (`python/password-reset-host`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/multiple/webapps/52485.txt
- r3j10r (Rajwinder Singh), osTicket 1.10.1 Arbitrary File Upload, EDB-45169,
  CVE-2017-15580 (`python/unrestricted-upload`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/windows/webapps/45169.txt
- RedTeam Pentesting, Ladon Framework for Python 0.9.40 XML External Entity
  Expansion, EDB-43113 (`python/xxe`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/xml/webapps/43113.txt
- nu11secur1ty, ever gauzy v0.281.9 JWT weak HMAC secret, EDB-51354
  (`python/jwt-default-key`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/typescript/webapps/51354.txt
- Dhrumil Mistry, djangorestframework-simplejwt inactive-user scenario,
  EDB-51992 (`python/jwt-disabled-user`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/python/webapps/51992.py
- Mohammed Aloraimi, Kimai 1.14 CSV Injection, EDB-49805
  (`python/csv-formula-injection`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/49805.txt
- Kacper Szurek / Shelby Pace, GitList 0.6.0 Argument Injection, EDB-44993
  (`python/argument-injection`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/remote/44993.rb
- Gangstuck / Psirac, Cscope insecure temporary file creation, EDB-24749
  (`python/file-create-race`):
  https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/linux/local/24749.sh

No Exploit-DB source code or affected application is vendored. These simplified
Python models do not claim to reproduce or validate the original products or CVE.

The REST API tenant-isolation extensions also reference Lawrence Amer's reports
on ProjectSend r754 client export IDOR (EDB-41433) and Chamilo message deletion
IDOR (EDB-39473). Only the general authorization failure patterns inform the
original fixtures; the tenant, queue and batch implementations are new:

- https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/41433.txt
- https://gitlab.com/exploit-database/exploitdb/-/blob/main/exploits/php/webapps/39473.txt

## Dependency laboratory fixtures

The dependency cases install `lodash.merge` 4.6.1 and 4.6.2 from npm using pinned
lockfiles. Lodash is distributed under the MIT license; its license and copyright
notices are included in the downloaded packages. Package source is not vendored here.
The `badass-settings-fixture` wrapper is original local benchmark code, not a
published third-party package.

Advisory reference: https://github.com/advisories/GHSA-h726-x36v-rx45

## MITRE Common Weakness Enumeration

`catalog/cwe.json` and the generated CWE matrix contain identifiers, names and
taxonomy metadata derived from the official MITRE CWE XML distribution, version
4.20, dated 2026-04-30. The imported XML SHA-256 is recorded in the catalog.

Copyright © 2006–2026, The MITRE Corporation. CWE is a trademark of The MITRE
Corporation.

CWE™ is free to use by any organization or individual for any research, development,
and/or commercial purposes, per these CWE Terms of Use. Accordingly, The MITRE
Corporation hereby grants you a non-exclusive, royalty-free license to use CWE for
research, development, and commercial purposes. Any copy you make for such purposes
is authorized on the condition that you reproduce MITRE’s copyright designation
and this license in any such copy. CWE is a trademark of The MITRE Corporation.

Source: https://cwe.mitre.org/data/downloads.html

Terms and disclaimers: https://cwe.mitre.org/about/termsofuse.html

## OWASP references

OWASP category identifiers and titles are attributed to their respective projects:

- Web Top 10:2025: https://top10.owasp.org/2025/0x00_2025-Introduction/
- API Security Top 10:2023: https://api-security.owasp.org/
- LLM Top 10:2025: https://genai.owasp.org/llm-top-10/

No OWASP explanatory text, training content or illustrations are copied. The
case mappings, code examples, test vectors and explanations are original project
content. This project is not endorsed or certified by MITRE or OWASP.
