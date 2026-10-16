#!/usr/bin/env python3
"""Render English documentation and complete coverage tables from the catalog."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from lab import coverage, read_catalog, validate
from runner import ROOT

LABELS = {'c': 'C', 'cpp': 'C++', 'go': 'Go', 'php': 'PHP', 'rest-api': 'REST API (Python handlers)',
          'node': 'Node.js', 'python': 'Python', 'cgi': 'CGI (Python)', 'dotnet': '.NET / C#',
          'typescript': 'TypeScript', 'java': 'Java', 'ruby': 'Ruby', 'rust': 'Rust', 'ai': 'AI / LLM boundaries'}
ORDER = list(LABELS)
NAMES = {'xss': 'Cross-site scripting (XSS)', 'sql-injection': 'SQL injection', 'xxe': 'XML external entities (XXE)',
         'idor': 'Insecure direct object reference (IDOR)', 'csrf': 'Cross-site request forgery (CSRF)',
         'ssrf': 'Server-side request forgery (SSRF)', 'bola': 'Broken object-level authorization (BOLA)',
         'cors-misconfiguration': 'Credentialed CORS misconfiguration', 'tls-verification': 'Disabled TLS verification',
         'header-injection': 'HTTP response header injection', 'missing-audit': 'Missing security audit events'}


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
    lines = ['# BADASS', '', '**Broken Application Designed for Auditing Security Scanners**', '',
             'An executable security benchmark for validating vulnerability detection and remediation across languages,',
             'REST APIs, CGI handlers and AI-assisted audit workflows. Each case includes deliberately vulnerable',
             'code, a corrected counterpart, benign inputs, attack inputs and machine-readable expectations.', '',
             f'**{len(cases)} case pairs · {len(LABELS)} technology sections · {covered} distinct CWE weaknesses · 30 OWASP categories represented**', '',
             'This is a local laboratory containing intentional vulnerabilities. Use synthetic data and the isolated',
             'container workflow. No service is exposed publicly, and no real credentials or external model calls are required.', '',
             '## Quick start', '', '```sh', '# Validate metadata and run the Python section with the installed runtime.',
             'python3 tools/lab.py validate', 'python3 tools/lab.py test --language python --strict', '',
             '# Build all runtimes, then run every case with external networking disabled.',
             'make container-build', 'make container-test', '```', '',
             'Python 3.11+ is sufficient for the tooling, Python, CGI, REST API and AI boundary sections.',
             'The full Linux suite uses GCC/G++, Go, PHP 8+, Node.js, TypeScript, .NET 8 SDK, JDK 17+, Ruby and Rust.',
             'Docker installs these runtimes without changing your host installation. The first image build needs network access.',
             'The container regression report is written to `reports/container-regression.json`.', '',
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
              'reports/       Generated execution and scoring reports (ignored by Git)',
              '.github/       CI validation and full isolated regression workflow', '```', '',
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
        for c in selected:
            slug=c['id'].split('/')[1]
            body.append(f"| [{title(c)}]({slug}/README.md) | {', '.join(c['cwe'])} | {', '.join(c['owasp'])} | {c['scope']} |")
            detail=[f'# {title(c)}', '', c['description'], '',
                    f"**Technology:** {LABELS[language]}  ", f"**CWE:** {', '.join(c['cwe'])}  ",
                    f"**OWASP:** {', '.join(c['owasp'])}  ", f"**Test scope:** `{c['scope']}`", '',
                    f"[Vulnerable source]({c['vulnerable'].split(c['id'] + '/')[1]}) · [Corrected source]({c['fixed'].split(c['id'] + '/')[1]})", '',
                    '## Correction', '', c['remediation'], '', '## Regression', '', '```sh',
                    f"python3 tools/lab.py test --case {c['id']} --strict", '```', '',
                    'Run from the repository root. Exact inputs and expected outputs are in',
                    '[the catalog](../../../catalog/cases.json). Both variants are tested.', '',
                    '| Vector | Type | Vulnerable expectation | Fixed expectation |', '|---|---|---|---|']
            for t in c['tests']:
                detail.append('| ' + ' | '.join(table_cell(x) for x in [t['name'],t['kind'],json.dumps(t['vulnerable'],ensure_ascii=False),json.dumps(t['fixed'],ensure_ascii=False)])+' |')
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
