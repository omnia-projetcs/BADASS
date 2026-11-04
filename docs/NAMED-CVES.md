# Named CVE teaching models

Seventeen case pairs cover documented runtime, framework and service vulnerabilities.
PHP2Shell has two separate cases because its two CVEs have different lifetime boundaries. Each case has
benign, attack and malformed-input vectors, a vulnerable implementation and a
corrected implementation.

These are original reduced models. They do not embed the affected PHP, Node.js,
Log4j, framework or service code and do not establish that those products were
exploited. Product-level exploit chains, heap grooming, ASLR bypass, real
LDAP/JNDI lookups and network services are outside their scope. The ImageTragick
case uses local printf commands to demonstrate actual shell interpretation. No exploit source
is copied. Native tests perform real invalid memory accesses in isolated child
processes under AddressSanitizer; the fixed variants must complete without those
diagnostics.

| Family | CVE | Case | Observable boundary |
|---|---|---|---|
| Log4Shell | CVE-2021-44228 | [Message lookup](../labs/python/log4shell-lookup/README.md) | A nested configuration expression reaches an offline naming callback; tests inspect the actual callback arguments and log bytes. |
| TeamCity | CVE-2024-27198 | [Dispatch authentication](../labs/python/teamcity-dispatch-bypass/README.md) | A public entry path forwards to an administrative handler and commits an unauthorized SQLite row. |
| PHP-CGI | CVE-2024-4577 | [Best-fit arguments](../labs/c/php-cgi-best-fit/README.md) | A modeled soft-hyphen conversion creates an option consumed by the real POSIX getopt parser. |
| Confluence | CVE-2022-26134 | [Pre-auth expressions](../labs/python/confluence-expression-dispatch/README.md) | Request-path evaluation exposes synthetic private state through a response header before login. |
| PHP2Shell | CVE-2026-109618 | [OOM cleanup](../labs/c/php2shell-oom/README.md) | An injected allocation failure and longjmp leave request cleanup with a dangling published pointer. |
| PHP2Shell | CVE-2026-109619 | [Stale worker state](../labs/c/php2shell-stale-state/README.md) | A fatal path or late shutdown callback leaves request-owned state visible to the next request on the same worker. |
| Node2Shell | CVE-2026-111497 | [Block-switch status](../labs/c/node2shell-block-switch/README.md) | Treating an invalid switch as input starvation keeps appending to an eight-byte heap buffer. |
| Spring4Shell | CVE-2022-22965 | [Class-loader binding](../labs/python/spring4shell-binding/README.md) | A client property traverses the internal model and redirects a real access log to a different local filename. |
| Jenkins CLI | CVE-2024-23897 | [Argument file expansion](../labs/python/jenkins-cli-atfile/README.md) | An error exposes a private file line expanded before the command's permission check. |
| FortiOS | CVE-2022-40684 | [Forwarded identity](../labs/python/fortios-forwarded-auth/README.md) | Client-supplied loopback headers authorize writing an administrator key marker. |
| Confluence setup | CVE-2023-22515 | [Setup-state binding](../labs/python/confluence-setup-reopen/README.md) | A public property changes persistent setup state and allows an unauthorized administrator row. |
| GitLab | CVE-2023-7028 | [Reset delivery](../labs/python/gitlab-reset-recipients/README.md) | A verified account match permits recovery-token delivery to an unverified recipient in the same request. |
| MinIO | CVE-2023-28432 | [Bootstrap disclosure](../labs/python/minio-bootstrap-disclosure/README.md) | Configuration and synthetic credentials are loaded before peer authentication. |
| ActiveMQ | CVE-2023-46604 | [Throwable construction](../labs/python/activemq-openwire-type/README.md) | A non-exception constructor parses an offline XML context and writes a file before type validation rejects it. |
| Zabbix | CVE-2024-42327 | [Role projection](../labs/python/zabbix-role-projection/README.md) | An authenticated SQL projection retrieves another role's token through a scalar subquery. |
| ImageTragick | CVE-2016-3714 | [Delegate shell](../labs/python/imagetragick-delegate/README.md) | A parsed SVG URL reaches a local shell delegate and creates a marker file. |
| Apache HTTP Server | CVE-2023-25690 | [Proxy request splitting](../labs/python/apache-proxy-request-splitting/README.md) | One decoded rewrite value produces two backend GET request lines in serialized bytes. |

## Additional model boundaries

The new handlers keep their dependencies local. The Spring4Shell model binds an
original dictionary graph, not Java introspection; the changed log prefix is
restricted to a local logs directory. The Jenkins model bounds file expansion to
small files within the fixture working directory and demonstrates one disclosed
line, without reproducing binary-key recovery or later Jenkins exploit chains.

The FortiOS key file contains synthetic markers, not working SSH keys. Confluence
setup tests cover persistent SQLite state across requests and a legitimate fresh
installation, configured by a trusted test environment variable. GitLab reset
deliveries are written to a local outbox; its constant token is a test marker and
does not model token entropy or send mail. MinIO configuration values are synthetic
and do not collect the host environment.

ActiveMQ uses a fixed original class registry and an offline XML map. It exercises
constructor effects before an exception-type check without loading Java classes
or remote XML. The Zabbix model uses real SQLite SQL and a small role table; it
does not implement the Zabbix API or subsequent privilege escalation. The
ImageTragick delegate only echoes a URL with /usr/bin/printf, never downloading
or converting images. Its attack vectors write synthetic local marker files.

The Apache proxy model parses a bounded GET/header grammar and writes its backend
request bytes to disk. It establishes a splitting boundary without network
services or claims about chunked transfer, request bodies, connection reuse or
all proxy parser behavior. Vendor severity descriptions remain authoritative;
for example, Apache describes CVE-2023-25690 as important rather than using a
uniform critical label for every case in this collection.

## Why the runtime cases are in C

PHP2Shell affects native runtime memory ownership, and Node2Shell affects the
native Brotli decoder used by Node.js. A PHP or JavaScript application that
merely calls eval, executes a command or performs ordinary decompression would
not reproduce those root causes. The C fixtures isolate their relevant ownership
and error-propagation mechanisms. The PHP-CGI fixture likewise isolates the
CGI-to-argv normalization boundary, with an explicit single-byte best-fit model
instead of claiming to invoke Windows codepage conversion.

PHP2Shell's OOM case injects failure into small allocations at two deterministic
stages; it does not exhaust machine memory. Its repair stages replacement data
and returns safely on failure. This is a reduced ownership correction, while
PHP's upstream repair changes its broader soft/hard OOM policy. The stale-state
case tests both early interruption and state republished by a later cleanup
callback, with controls for no second consumer and for a fresh worker.

Node2Shell's input syntax is `category/type-count/payload`, not a Brotli bitstream.
It covers literal, command and distance paths. Both short malformed feeds and the
ninth buffered byte are tested. Adding only a buffer bound would stop the write
but still misclassify an impossible switch as temporary input starvation; the
short-feed tests reject that incomplete repair.

## Upstream identity and remediation

The CVE identity and scope come from upstream security advisories. The following
are advisory-specific fix boundaries, not a recommendation to install an older
release instead of a currently supported security update. Vendor backports can
also change the status of an individual package.

- PHP2Shell: [CVE-2026-109618, OOM corruption](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w)
  and [CVE-2026-109619, stale global state](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp).
  PHP's [21 October 2026 release announcement](https://www.php.net/archive/2026.php)
  identifies PHP 8.2.35, 8.3.36, 8.4.27 and 8.5.12 as fixes for these two CVEs.
  Other session-handling follow-up advisories are separate from these two models.
- Node2Shell: [Node.js October 2026 security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
  identifies CVE-2026-111497 and fixed Node.js releases 22.23.4, 24.22.1 and
  26.12.1. Node.js rates the issue **high**; severity terminology should retain
  that vendor context. The [Brotli correction](https://github.com/google/brotli/commit/0ed4268a4401abcb4472096340477cf4af7d1a2b)
  distinguishes a permanent block-switch error from temporary input starvation.
  Upstream released [Brotli 1.2.1](https://github.com/google/brotli/releases/tag/v1.2.1),
  with fixes also backported to the 1.0 and 1.1 branches.
- PHP-CGI: the [PHP advisory for CVE-2024-4577](https://github.com/php/php-src/security/advisories/GHSA-3qgc-jrrr-25jv)
  describes the Windows best-fit argument bypass and the affected deployment
  conditions. This is distinct from PHP2Shell's 2026 memory defects.
- Log4Shell: the [Apache Log4j security page](https://logging.apache.org/security.html)
  describes CVE-2021-44228 and later related advisories. The fixture does not
  claim that an application wrapper substitutes for upgrading log4j-core.
- TeamCity: [JetBrains' CVE-2024-27198 advisory](https://blog.jetbrains.com/teamcity/2024/03/additional-critical-security-issues-affecting-teamcity-on-premises-cve-2024-27198-and-cve-2024-27199-update-to-2023-11-4-now/)
  identifies authentication bypass and administrative access. Only CVE-2024-27198
  is represented here; CVE-2024-27199 is outside this model.
- Confluence: [Atlassian's CVE-2022-26134 advisory](https://confluence.atlassian.com/doc/confluence-security-advisory-2022-06-02-1130377146.html)
  describes the pre-authentication expression-injection vulnerability. The
  benchmark uses an original limited interpreter, not OGNL or Java class loading.
- Spring4Shell: [Spring's CVE-2022-22965 advisory](https://spring.io/security/cve-2022-22965/)
  explains the data-binding issue and the prerequisites of the demonstrated
  JDK/Tomcat/WAR exploit. The fixture models only unauthorized property traversal.
- Jenkins: [the 2024-01-24 security advisory](https://www.jenkins.io/security/advisory/2024-01-24/)
  documents CVE-2024-23897, args4j @file expansion and the permission-dependent
  disclosure limits.
- FortiOS: [FG-IR-22-377](https://www.fortiguard.com/psirt/FG-IR-22-377) identifies
  CVE-2022-40684. [EDB-51092](https://www.exploit-db.com/exploits/51092) documents
  the forwarded loopback-header pattern used to inform the original fixture.
- Confluence setup: [Atlassian's CVE-2023-22515 advisory](https://confluence.atlassian.com/security/cve-2023-22515-broken-access-control-vulnerability-in-confluence-data-center-and-server-1295682276.html)
  and [EDB-51829](https://www.exploit-db.com/exploits/51829) identify the separate
  setup-related access-control flaw.
- GitLab: [its CNA record for CVE-2023-7028](https://gitlab.com/gitlab-org/cves/-/blob/40bb099b1d6622fad9a67a2ed4e4c7addc9388a2/2023/CVE-2023-7028.json)
  identifies recovery-token delivery to unverified email addresses.
- MinIO: [its CVE-2023-28432 advisory](https://github.com/minio/minio/security/advisories/GHSA-6xvq-wj2x-3h3q)
  documents distributed-bootstrap configuration disclosure and the need to
  validate internode tokens.
- ActiveMQ: [Apache's CVE-2023-46604 explanation](https://activemq.apache.org/news/cve-2023-46604)
  describes class instantiation while unmarshalling a throwable. The fixture's
  XML context loader is an original local analogue of constructor side effects.
- Zabbix: [ZBX-25623](https://support.zabbix.com/browse/ZBX-25623) documents
  CVE-2024-42327, SQL injection reachable by users with API access.
- ImageTragick: [the original researcher disclosure](https://imagetragick.com/)
  and [EDB-39767](https://www.exploit-db.com/exploits/39767) document the delegate
  command boundary for CVE-2016-3714. Other ImageMagick CVEs in that report are
  outside this individual case.
- Apache HTTP Server: [the upstream CVE-2023-25690 record](https://httpd.apache.org/security/json/CVE-2023-25690.json)
  describes reinsertion of a captured request target by rewrite/proxy rules.

## Regression

Run from the repository root with Python 3.11+ and GCC/AddressSanitizer installed:

```sh
python3 tools/lab.py validate
python3 -m unittest discover -s tests -p test_named_cves.py -v
python3 -m unittest discover -s tests -p test_cve_extensions.py -v
python3 tools/export_training.py --check
python3 tools/render_docs.py --check
```

The dedicated test modules run every named-CVE vector in both variants and check
independent evidence, including native diagnostics, a deliberately incomplete
Node2Shell repair, actual log bytes, SQLite rows and expression callback calls.
No PHP, Node.js, Java product installation or external network is required for
these reduced models. All source pairs also participate in the normal C and
Python regression sections and in scanner exports.
