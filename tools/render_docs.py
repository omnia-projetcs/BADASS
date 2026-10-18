#!/usr/bin/env python3
"""Render English documentation and complete coverage tables from the catalog."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from lab import coverage, read_catalog, read_plan, validate
from runner import ROOT

LABELS = {'c': 'C', 'cpp': 'C++', 'go': 'Go', 'php': 'PHP', 'rest-api': 'REST API (Python handlers)',
          'node': 'Node.js', 'python': 'Python', 'cgi': 'CGI (Python)', 'dotnet': '.NET / C#',
          'typescript': 'TypeScript', 'java': 'Java', 'ruby': 'Ruby', 'rust': 'Rust', 'ai': 'AI / LLM boundaries'}
ORDER = list(LABELS)
NAMES = {'xss': 'Cross-site scripting (XSS)', 'sql-injection': 'SQL injection', 'xxe': 'XML external entities (XXE)',
         'idor': 'Insecure direct object reference (IDOR)', 'csrf': 'Cross-site request forgery (CSRF)',
         'ssrf': 'Server-side request forgery (SSRF)', 'bola': 'Broken object-level authorization (BOLA)',
         'cors-misconfiguration': 'Credentialed CORS misconfiguration', 'tls-verification': 'Disabled TLS verification',
         'header-injection': 'HTTP response header injection', 'missing-audit': 'Missing security audit events',
         'business-logic': 'Invalid purchase quantity', 'sql-order-by': 'SQL injection in an ORDER BY identifier',
         'sql-second-order': 'Second-order SQL injection', 'xss-attribute': 'XSS in an HTML attribute',
         'ssrf-redirect': 'SSRF through an HTTP redirect', 'order-concurrency': 'Concurrent duplicate shipment'}


def title(case):
    slug = case['id'].split('/')[1]
    return NAMES.get(slug, slug.replace('-', ' ').capitalize())


def table_cell(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ')


def render():
    cases = read_catalog()
    validate(cases)
    report = coverage(cases)
    cwe_count = sum(row['kind'] == 'weakness' for row in report['cwe'])
    covered = report['counts']['implemented']
    matrix = report['by_technology']
    plan = read_plan()
    core = next(g for g in plan['groups'] if g['id'] == 'common-core')
    core_ids = set(core['cwe'])
    badges = [
        '[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)',
        '[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)',
        '[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](Dockerfile)',
        f'[![Benchmark Cases](https://img.shields.io/badge/Cases-{len(cases)}%20pairs-brightgreen.svg)](catalog/cases.json)',
        f'[![Technologies](https://img.shields.io/badge/Technologies-{len(LABELS)}%20stacks-informational.svg)](docs/TECHNOLOGY-MATRIX.md)',
        f'[![CWE Weaknesses](https://img.shields.io/badge/CWE-{covered}%20weaknesses-orange.svg)](docs/CWE-MATRIX.md)',
        '[![OWASP Coverage](https://img.shields.io/badge/OWASP-30%20categories-red.svg)](docs/OWASP-MATRIX.md)',
        '[![Benchmark Methodology](https://img.shields.io/badge/Benchmark-Methodology-blueviolet.svg)](docs/BENCHMARK.md)',
    ]
    topics_line = '> **GitHub Topics & Tags:** `security-benchmark` · `vulnerability-detection` · `sast` · `dast` · `cwe` · `owasp` · `appsec` · `security-scanner` · `code-auditing` · `static-analysis` · `security-testing` · `docker`'
    lines = ['# BADASS', '', '**Broken Application Designed for Auditing Security Scanners**', '',
             *badges, '',
             topics_line, '',
             'An executable security benchmark for validating vulnerability detection and remediation across languages,',
             'REST APIs, CGI handlers and AI-assisted audit workflows. Each case includes deliberately vulnerable',
             'code, a corrected counterpart, benign inputs, attack inputs and machine-readable expectations.',
             'Functional and robustness vectors also check useful operations and malformed input.', '',
             f'**{len(cases)} case pairs · {len(LABELS)} technology sections · {covered} distinct CWE weaknesses · 30 OWASP categories represented**', '',
             'This is a local laboratory containing intentional vulnerabilities. Use synthetic data and the isolated',
             'container workflow. No service is exposed publicly, and no real credentials or external model calls are required.', '',
             '## Quick start', '', '```sh', '# Validate metadata and run the Python section with the installed runtime.',
             'python3 tools/lab.py validate', 'python3 tools/lab.py test --language python --strict', '',
             '# Run the mandatory nonempty smoke gate.', 'make smoke', '',
             '# Build all runtimes, then run every case with external networking disabled.',
             'make container-build', 'make container-test', '```', '',
             'Python 3.11+ is sufficient for the tooling, Python, CGI, REST API and AI boundary sections.',
             'The full Linux suite uses GCC/G++, Go, PHP 8+, Node.js, TypeScript, .NET 8 SDK, JDK 17+, Ruby and Rust.',
             'Docker installs these runtimes without changing your host installation. The first image build needs network access.',
             'The container regression report is written to `reports/container-regression.json`.', '',
             '**SQL injection (CWE-89) is implemented in every technology section**, using actual SQLite queries',
             'and parameter-bound corrections. The image includes the required language drivers.',
             'Run all SQL injection cases with:', '', '```sh',
             "make container-test LAB_ARGS='test --cwe CWE-89 --strict --output reports/sql-injection.json'", '```', '',
             'See [SQL injection cases, drivers and test coverage](docs/SQL-INJECTION.md).', '',
             '## Vulnerable dependencies', '',
             'Two executable Node.js cases cover **CWE-1395**: a [direct dependency](labs/node/vulnerable-dependency/README.md)',
             'and a [transitive dependency](labs/node/vulnerable-transitive-dependency/README.md).',
             'Both use real pinned `lodash.merge` releases, package manifests and integrity-checked lockfiles.',
             'The correction upgrades the dependency while retaining the same application code.', '',
             '```sh',
             'make dependency-prepare  # Install pinned packages; needs npm registry access on a cold cache.',
             'make dependency-test     # 24 variant/vector checks; no network required.',
             '```', '',
             'Prepare these packages before running the Node.js section with the general runner.',
             'See [dependency fixtures, advisory and SCA evaluation](docs/DEPENDENCIES.md).', '',
             '## Exploit-DB inspired cases', '',
             'Ten original Python fixtures model weaknesses documented in public Exploit-DB entries:', '',
             '- [SQL login bypass](labs/python/sql-login-bypass/README.md) (EDB-41029).',
             '- [ZIP extraction traversal](labs/python/zip-slip/README.md) (EDB-39816).',
             '- [Password-reset Host poisoning](labs/python/password-reset-host/README.md) (EDB-52485).',
             '- [Unrestricted upload](labs/python/unrestricted-upload/README.md) (EDB-45169).',
             '- [XML external entity file disclosure](labs/python/xxe/README.md) (EDB-43113).',
             '- [Default JWT signing key](labs/python/jwt-default-key/README.md) (EDB-51354).',
             '- [JWT accepted for a disabled account](labs/python/jwt-disabled-user/README.md) (EDB-51992).',
             '- [CSV formula injection](labs/python/csv-formula-injection/README.md) (EDB-49805).',
             '- [Child-process argument injection](labs/python/argument-injection/README.md) (EDB-44993).',
             '- [File creation race](labs/python/file-create-race/README.md) (EDB-24749).', '',
             'Each includes a corrected counterpart, synthetic inputs and regression expectations.',
             'These are teaching models, not reproductions of the affected products. Source references',
             'and scope limits appear in each case README.', '',
             'The [Python format-string disclosure](labs/python/format-string-disclosure/README.md)',
             'case additionally exercises real attribute traversal through `str.format`, with a',
             'restricted public-placeholder correction. See [general boundary cases](docs/GENERAL-BOUNDARIES.md).', '',
             '## Tenant isolation', '',
             'Seven REST API handler cases exercise cross-tenant cache leaks, tenant-scoped roles,',
             'export-worker scope loss, mixed-tenant batch updates, signed download scope,',
             'session switching and storage path boundaries.',
             'Tests inspect real exported files, account snapshots and committed SQLite rows.',
             'See [tenant isolation scenarios and regression commands](docs/TENANT-ISOLATION.md).', '',
             '## Coverage by technology', '',
             f'The shared baseline targets **{len(core_ids)} weakness families in all {len(LABELS)} sections**.',
             'C and C++ also have explicit native memory, format-string and integer-arithmetic targets.',
             'Counts below come from exact CWE mappings. They describe source pairs and regression vectors;',
             'execution results remain in the regression reports.', '',
             '| Technology | Case pairs | Distinct CWE | Shared baseline | Planned targets |',
             '|---|---:|---:|---:|---:|']
    for language in ORDER:
        s = matrix['summary'][language]
        implemented = {w for c in cases if c['language'] == language for w in c['cwe']}
        lines.append(f"| [{LABELS[language]}](labs/{language}/README.md) | {s['cases']} | {s['implemented']} | "
                     f"{len(core_ids & implemented)}/{len(core_ids)} | {s['targets_implemented']}/{s['targets']} |")
    lines += ['', 'See the [baseline and native targets](docs/CORE-MATRIX.md) and the',
              '[complete CWE × technology matrix](docs/TECHNOLOGY-MATRIX.md).',
              'The latter includes every weakness in the pinned taxonomy. Missing cases outside the declared',
              'targets remain `unassessed`; this does not mean they are impossible in that language.', '',
             '## Vulnerabilities by technology', '',
             'Every vulnerability currently implemented is listed below. Links open the case documentation, including',
             'the vulnerable and corrected source files. A case in the table is not a claim of full CWE coverage.', '',
              '| Technology | Cases | Implemented vulnerabilities (CWE) |', '|---|---:|---|']
    for language in ORDER:
        selected = [c for c in cases if c['language'] == language]
        entries = [f"[{title(c)}](labs/{c['id']}/README.md) ({', '.join(c['cwe'])})" for c in selected]
        lines.append(f"| [{LABELS[language]}](labs/{language}/README.md) | {len(selected)} | " + '<br>'.join(entries) + ' |')
    lines += ['', '## What coverage means', '',
              f'The [complete CWE matrix](docs/CWE-MATRIX.md) enumerates all **{len(report["cwe"])} entries** from MITRE CWE',
              f'**{report["cwe_version"]}**: **{cwe_count} weaknesses** plus categories and views. **{covered} weaknesses** currently',
              f'have direct executable cases; **{report["counts"]["gap"]} remain explicit gaps**. Categories and views are marked',
              '`taxonomy-only`. The matrix is exhaustive for this snapshot; the executable corpus is not.', '',
              'The [OWASP matrix](docs/OWASP-MATRIX.md) tracks all categories in **Web Top 10:2025**,',
              '**API Security Top 10:2023**, and **LLM Top 10:2025**. Each has at least one mapped example.',
              'These are pinned editions, not a claim to cover every OWASP project or every scenario within a category.',
              'ASVS, WSTG, mobile, hardware and other domains still require additional work.', '',
              'Most language cases are small executable source slices. API cases mainly exercise handler boundaries;',
              'the SSRF case includes a real loopback HTTP request. AI boundary tests run application controls, not a model.',
              'See [benchmark methodology and assumptions](docs/BENCHMARK.md).', '',
              '## Run, score and repair', '', '```sh',
              'python3 tools/lab.py list --language java',
              'python3 tools/lab.py test --case java/xxe --strict',
              'python3 tools/lab.py test --cwe CWE-89 --strict --output reports/sql-injection.json',
              'python3 tools/lab.py test --strict --output reports/regression.json',
              'python3 tools/lab.py coverage --output reports/coverage.json',
              'python3 tools/lab.py score --findings findings.json --output reports/score.json',
              'python3 -m unittest discover -s tests -v', '```', '',
              'The runner checks both variants against the same vectors. A missing runtime is reported as `skip`;',
              '`--strict` turns skips into failures. Failed builds, timeouts and unrelated crashes never count as successful tests.',
              'C/C++ memory cases use AddressSanitizer and UndefinedBehaviorSanitizer.', '',
              'The scorer accepts normalized findings with `case_id`, `variant`, and `cwe`. It reports precision, recall,',
              'false positives and false negatives, deduplicating repeated findings. See the [input format](docs/BENCHMARK.md#detection-scoring).',
              'Evaluate a candidate correction in the `fixed/` source while keeping test expectations trusted and unchanged.', '',
              'File expectations inspect real contents, file types and permissions after execution. Trusted oracles',
              'exercise password, reset-token and session operations without accepting a candidate self-assessment.',
              'An empty selection or an entirely skipped execution cannot pass. See the',
              '[correction notes](docs/REVIEW-CHANGES.md) and [French application guide](GUIDE_CORRECTIONS_FR.md).', '',
              'For a scanner corpus without case/variant directory labels, keep the mapping outside the exported directory:', '',
              '```sh',
              'python3 tools/export_blind.py --output ../badass-blind --mapping ../badass-blind-map.json',
              '```', '',
              'The exporter preserves source bytes. It removes directory labels and documentation, not all possible',
              'semantic clues in code; it does not establish that a scanner or model has never seen the sources.', '',
              '## AI prompt injection, reverse repair injection and jailbreaks', '',
              'Ten [inert attack payloads](catalog/ai-attacks.json) cover direct overrides, authority spoofing, roleplay,',
              'encoded jailbreaks, source comments, retrieval content, tool responses, synthetic canary requests,',
              'unauthorized tool escalation and instructions to introduce vulnerabilities during a repair.', '',
              'The [AI evaluation protocol](docs/AI-TESTING.md) explains how to collect independent observations and score',
              'finding suppression, disclosure, unauthorized actions and repair regressions:', '', '```sh',
              'python3 tools/ai_evaluate.py observations.json --output reports/ai-evaluation.json', '```', '',
              'No real-model resilience result is claimed. Missing observations remain untested. Application boundary',
              'tests do not prove that an LLM resists prompt injection or jailbreaks.', '',
              '## Repository layout', '', '```text',
              'catalog/       Case contracts, CWE snapshot, OWASP references and AI attack manifest',
              'labs/          One section per technology; vulnerable/ and fixed/ source pairs',
              'tools/         Regression runner, scorer, CWE importer and documentation renderer',
              'tests/         Regression tests for the benchmark tooling itself',
              'docs/          Complete CWE matrix, OWASP mappings and evaluation protocols',
              'reports/       Generated execution and scoring reports (ignored by Git)', '```', '',
              '## Add a case or update the catalog', '',
              '1. Add a focused source pair under `labs/<technology>/<case>/{vulnerable,fixed}/`.',
              '2. Add an entry to `catalog/cases.json` with its CWE, OWASP mappings, scope, remediation and test vectors.',
              '3. Include at least one benign vector and one attack vector with different vulnerable/fixed outcomes.',
              '4. Run catalog validation, the affected regression, tooling tests and `python3 tools/render_docs.py`.',
              '5. Keep limitations explicit; do not label unimplemented weaknesses as covered.', '',
              'To refresh the CWE snapshot, download an official XML ZIP from [MITRE](https://cwe.mitre.org/data/downloads.html),',
              'then run `python3 tools/import_cwe.py /path/to/cwec_VERSION.xml.zip` and regenerate the documentation.',
              'Review mappings, metadata and third-party notices when changing reference versions.', '',
              '## References and license', '',
              '- [MITRE CWE downloads](https://cwe.mitre.org/data/downloads.html)',
              '- [OWASP Web Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/)',
              '- [OWASP API Security Top 10:2023](https://api-security.owasp.org/)',
              '- [OWASP LLM Top 10:2025](https://genai.owasp.org/llm-top-10/)', '',
              'Project code: [MIT License](LICENSE). Taxonomy data and reference attribution:',
              '[third-party notices](THIRD_PARTY_NOTICES.md). No MITRE or OWASP endorsement is implied.', '']
    outputs = {'README.md': '\n'.join(lines)}
    for language in ORDER:
        selected = [c for c in cases if c['language'] == language]
        body = [f'# {LABELS[language]}', '', '[Project overview](../../README.md) · [Methodology](../../docs/BENCHMARK.md)', '',
                '```sh', f'python3 tools/lab.py test --language {language} --strict', '```', '',
                'Run commands from the repository root. Cases are independent and use synthetic fixtures.', '',
                '| Vulnerability | CWE | OWASP | Scope |', '|---|---|---|---|']
        if language == 'node':
            body[body.index('| Vulnerability | CWE | OWASP | Scope |'):body.index('| Vulnerability | CWE | OWASP | Scope |')] = [
                'For the direct and transitive dependency cases, use `make dependency-prepare` then',
                '`make dependency-test`. Prepare these packages before using the general runner.',
                'See [dependency setup and SCA evaluation](../../docs/DEPENDENCIES.md).', '']
        for c in selected:
            slug=c['id'].split('/')[1]
            body.append(f"| [{title(c)}]({slug}/README.md) | {', '.join(c['cwe'])} | {', '.join(c['owasp'])} | {c['scope']} |")
            if c.get('dependency'):
                # Dependency cases have hand-written setup and SCA instructions.
                continue
            detail=[f'# {title(c)}', '', c['description'], '',
                    '| Attribute | Value |', '|---|---|',
                    f"| Technology | {LABELS[language]} |", f"| CWE | {', '.join(c['cwe'])} |",
                    f"| OWASP | {', '.join(c['owasp'])} |", f"| Test scope | `{c['scope']}` |", '',
                    f"[Vulnerable source]({c['vulnerable'].split(c['id'] + '/')[1]}) · [Corrected source]({c['fixed'].split(c['id'] + '/')[1]})", '',
                    '## Correction', '', c['remediation'], '', '## Regression', '', '```sh',
                    f"python3 tools/lab.py test --case {c['id']} --strict", '```', '',
                    'Run from the repository root. Exact inputs and expected outputs are in',
                    '[the catalog](../../../catalog/cases.json). Both variants are tested.', '',
                    'The runner also checks every declared file effect. `functional` vectors can specify a useful',
                    'operation that the vulnerable implementation did not support correctly; `robustness` vectors',
                    'exercise malformed inputs. `benign` vectors require identical expectations.', '',
                    '| Vector | Type | Vulnerable expectation | Fixed expectation |', '|---|---|---|---|']
            if c.get('oracle'):
                detail[detail.index('| Vector | Type | Vulnerable expectation | Fixed expectation |'):detail.index('| Vector | Type | Vulnerable expectation | Fixed expectation |')] = [
                    f"Trusted oracle: `{c['oracle']}`. Vector `context` is supplied by the harness outside candidate input.", '']
            for t in c['tests']:
                detail.append('| ' + ' | '.join(table_cell(x) for x in [t['name'],t['kind'],json.dumps(t['vulnerable'],ensure_ascii=False),json.dumps(t['fixed'],ensure_ascii=False)])+' |')
            if c.get('references'):
                detail += ['', '## Inspiration and provenance', '',
                           'Original benchmark implementation inspired by the documented weakness;',
                           'no third-party exploit source is copied or executed.', '']
                detail += [f"- [{ref['title']}]({ref['url']})" for ref in c['references']]
            detail+=['','This example demonstrates the declared weakness within the documented fixture assumptions.',
                     'It is not a production application or a proof that every related attack is prevented.', '',
                     '[Technology index](../README.md) · [Benchmark methodology](../../../docs/BENCHMARK.md)', '']
            outputs[f"labs/{c['id']}/README.md"]='\n'.join(detail)
        outputs[f'labs/{language}/README.md']='\n'.join(body)+'\n'
    lines=['# Complete CWE coverage matrix', '',
           f"Source: MITRE CWE **{report['cwe_version']}**. All **{len(report['cwe'])}** entries from the imported snapshot are included.", '',
           f"**{covered} implemented weaknesses**, **{report['counts']['gap']} gaps**, **{report['counts']['taxonomy-only']} category/view entries**.", '',
           '`implemented` means source pairs and vectors exist, not that a scanner detected them or a runtime was available.',
           'Test results are tracked separately. `gap` is an unimplemented weakness. `taxonomy-only` is a category or view.',
           'Deprecated entries remain visible with their MITRE status. No coverage is inherited from parent categories.', '',
           '[Machine-readable snapshot](../catalog/cwe.json) · [Attribution and license](../THIRD_PARTY_NOTICES.md)', '',
           '| CWE | Name | Kind | MITRE status | Coverage | Cases |', '|---|---|---|---|---|---|']
    for r in report['cwe']:
        case_links=', '.join(f'[{cid}](../labs/{cid}/README.md)' for cid in r['cases'])
        lines.append('| '+ ' | '.join(table_cell(x) for x in [r['id'],r['name'],r['kind'],r['status'],r['coverage'],case_links])+' |')
    outputs['docs/CWE-MATRIX.md']='\n'.join(lines)+'\n'
    technology_header = '| CWE | Weakness | ' + ' | '.join(LABELS[lang] for lang in ORDER) + ' |'
    technology_separator = '|---|---|' + '---|' * len(ORDER)

    def technology_row(row):
        cells = []
        for language in ORDER:
            cell = row['technologies'][language]
            cells.append('<br>'.join(f'[{cid.split("/", 1)[1]}](../labs/{cid}/README.md)'
                                    for cid in cell['cases']) or cell['status'])
        return '| ' + ' | '.join([row['id'], table_cell(row['name']), *cells]) + ' |'

    lines = ['# Complete CWE × technology matrix', '',
             f"MITRE CWE **{report['cwe_version']}**: **{len(matrix['rows'])} weaknesses × {len(ORDER)} technology sections**.", '',
             'A linked case is implemented in that exact section. `gap` means a declared target has no case.',
             '`unassessed` means there is no case and applicability has not been reviewed. Neither absence',
             'status means not applicable. No coverage is inherited from parents, other languages or OWASP categories.',
             'Deprecated weaknesses remain included. Categories and views are listed in the [taxonomy matrix](CWE-MATRIX.md).', '',
             'Implementation is source/vector evidence; runtime pass/fail evidence is stored separately in reports.',
             'The AI, REST API and CGI columns are Python application contexts, not additional programming languages.', '',
             '[Declared targets](../catalog/coverage-plan.json) · [Target summary](CORE-MATRIX.md) · [Methodology](BENCHMARK.md)', '',
             technology_header, technology_separator]
    lines += [technology_row(row) for row in matrix['rows']]
    outputs['docs/TECHNOLOGY-MATRIX.md'] = '\n'.join(lines) + '\n'
    lines = ['# Shared baseline and native coverage targets', '', plan['scope'], '',
             'These are finite implementation targets, not a count of all possible vulnerabilities.',
             'Every link refers to a source pair with benign and attack vectors. See the',
             '[complete per-technology matrix](TECHNOLOGY-MATRIX.md) for weaknesses outside these targets.', '',
             '[Machine-readable plan](../catalog/coverage-plan.json)', '']
    by_id = {row['id']: row for row in matrix['rows']}
    for group in plan['groups']:
        lines += [f"## {group['id']}", '', group['scope'], '',
                  'Target sections: ' + ', '.join(LABELS[lang] for lang in group['technologies']) + '.', '',
                  technology_header, technology_separator]
        lines += [technology_row(by_id[w]) for w in group['cwe']]
        lines.append('')
    outputs['docs/CORE-MATRIX.md'] = '\n'.join(lines)
    lines=['# OWASP coverage matrix', '',
           'Project-maintained mappings to pinned editions. A mapped example is not exhaustive category coverage.',
           'Scope distinguishes executable sinks, handler models, configuration checks and AI application boundaries.', '',
           'Other OWASP projects, including ASVS and WSTG, are not claimed as fully covered.', '']
    for framework in json.loads((ROOT/'catalog/frameworks.json').read_text()):
        lines += [f"## {framework['id']}", '', f"[Official reference]({framework['source']})", '',
                  '| Category | Title | Cases and scopes |', '|---|---|---|']
        for key,label in framework['categories'].items():
            selected=[c for c in cases if key in c['owasp']]
            links='<br>'.join(f"[{c['id']}](../labs/{c['id']}/README.md) — {c['scope']}" for c in selected) or 'GAP'
            lines.append(f'| {key} | {label} | {links} |')
        lines.append('')
    outputs['docs/OWASP-MATRIX.md']='\n'.join(lines)
    return outputs


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    stale=[]
    for relative,content in render().items():
        path=ROOT/relative
        if args.check:
            if not path.exists() or path.read_text()!=content:
                stale.append(relative)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content)
    if stale:
        print('Outdated generated documentation:', ', '.join(stale))
        sys.exit(1)
    print('Documentation is current.' if args.check else 'Documentation generated.')
