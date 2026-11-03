# Third-party notices

Original project code is covered by [LICENSE](LICENSE).

## Named CVE teaching models

The seven named-CVE cases covering Log4Shell, TeamCity, PHP-CGI, Confluence,
PHP2Shell and Node2Shell are original reduced implementations. They reference
upstream advisories and, for Brotli, the upstream correction to identify the
failure mechanism. No PHP, Node.js, Brotli, Log4j, TeamCity, Confluence or
third-party exploit source is vendored or copied into these fixtures.

- PHP Group / PHP security team, CVE-2026-109618 (OOM corruption):
  https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w
- PHP Group / PHP security team, CVE-2026-109619 (stale global state):
  https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp
- Node.js / Google Brotli, CVE-2026-111497 (Node2Shell):
  https://nodejs.org/en/blog/vulnerability/october-2026-security-releases
  https://github.com/google/brotli/commit/0ed4268a4401abcb4472096340477cf4af7d1a2b
- Orange Tsai / DEVCORE and PHP Group, CVE-2024-4577 (Windows CGI arguments):
  https://github.com/php/php-src/security/advisories/GHSA-3qgc-jrrr-25jv
- Apache Logging Services, CVE-2021-44228 (Log4Shell):
  https://logging.apache.org/security.html
- JetBrains / Rapid7, CVE-2024-27198 (TeamCity authentication bypass):
  https://blog.jetbrains.com/teamcity/2024/03/additional-critical-security-issues-affecting-teamcity-on-premises-cve-2024-27198-and-cve-2024-27199-update-to-2023-11-4-now/
- Atlassian, CVE-2022-26134 (Confluence expression injection):
  https://confluence.atlassian.com/doc/confluence-security-advisory-2022-06-02-1130377146.html

The Log4Shell, TeamCity, PHP-CGI and Confluence models also reference EDB-51183,
EDB-52411, EDB-52331 and EDB-50952 respectively. Those reports are cited in each
case README; their exploit code is not included. The PHP2Shell and Node2Shell
models rely on the upstream references above and claim no invented Exploit-DB
identifier. See [model boundaries and provenance](docs/NAMED-CVES.md).

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
- Lucas Souza, Apache HTTP Server 2.4.50 path traversal, EDB-50406,
  CVE-2021-42013 (`python/double-decoding-traversal`):
  https://www.exploit-db.com/exploits/50406
- tmrswrr, Akaunting 3.1.8 template expression injection, EDB-52030
  (`python/item-template-injection`):
  https://www.exploit-db.com/exploits/52030
- sirpedrotavares, CHIYU TCP/IP Converter CRLF injection, EDB-49923
  (`python/cgi-redirect-splitting`):
  https://www.exploit-db.com/exploits/49923
- Jorge González Milla (Pig-Tail), flyto_core 2.26.7 DNS rebinding SSRF,
  EDB-52651 (`python/dns-rebinding-ssrf`):
  https://www.exploit-db.com/exploits/52651
- 9tamilmathi (Tamil Mathi T.), ThingsBoard 4.2.0 SVG resource SSRF,
  EDB-52551, CVE-2025-34282 (`python/svg-resource-ssrf`):
  https://www.exploit-db.com/exploits/52551
- Emir Polat, CVAT remote-file import SSRF, EDB-51030, CVE-2022-31188
  (`python/remote-import-ssrf`):
  https://www.exploit-db.com/exploits/51030
- Andrey B. Panfilov, OpenText Documentum TAR symlink traversal, EDB-43002,
  CVE-2017-15276 (`python/tar-symlink-escape`):
  https://www.exploit-db.com/exploits/43002
- Gergely Eberhardt, Ubee EVW3226 1.0.20 factoryBypass authentication bypass,
  EDB-40156 (`python/factory-auth-bypass`):
  https://www.exploit-db.com/exploits/40156
- SecuriTeam / Francis Alexander, OrientDB query-clause permission bypass,
  EDB-44068, CVE-2017-11467 (`python/query-clause-authorization`):
  https://www.exploit-db.com/exploits/44068
- Andrew Gill, Oracle E-Business Suite backslash open redirect, EDB-43592,
  CVE-2017-3528 (`python/backslash-open-redirect`):
  https://www.exploit-db.com/exploits/43592

No Exploit-DB source code or affected application is vendored. These simplified
Python models do not claim to reproduce or validate the original products or CVE.
The three new SSRF cases use an offline DNS/endpoint registry rather than real
network requests. The template case uses a bounded original arithmetic engine.
The OrientDB-inspired case covers the query authorization stage only. Detailed
assumptions and exclusions are recorded in each case's remediation and README.

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
