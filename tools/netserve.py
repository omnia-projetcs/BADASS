#!/usr/bin/env python3
"""Expose catalog fixtures as opaque HTTP targets for network-only (black-box) evaluation.

Every case variant (vulnerable and fixed) is published under a random target id.
Clients only see HTTP: a discovery document with benign seed requests, and the
responses of the fixture. The answer key (target id -> case/variant) is written
to a private mapping file that must never be given to the scanner.

Interfaces published in /targets.json:
  json   POST /t/<id> with a JSON body (Python, REST API and AI sections)
  query  GET  /t/<id>?<raw query string> (CGI section, raw QUERY_STRING)
  param  GET  /t/<id>?input=<value> or POST text/plain (native sections)
"""
import argparse
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab import read_catalog, validate  # noqa: E402
from runner import ROOT, RUNTIMES, prepare, process  # noqa: E402

STRUCTURED = {"python", "cgi", "rest-api", "ai"}
CRASH_MARKERS = ("AddressSanitizer", "UndefinedBehaviorSanitizer", "runtime error:",
                 "Segmentation fault", "panicked at", "stack smashing")
MAX_BODY = 1 << 20


def interface(case):
    if case["language"] == "cgi":
        return "query"
    return "json" if case["language"] in STRUCTURED else "param"


def deployment(case):
    """Deployment configuration comes from benign vectors only, never from attacks."""
    benign = [t for t in case["tests"] if t["kind"] == "benign"]
    env = next((t["env"] for t in benign if t.get("env")), {})
    context = next((t["context"] for t in benign if t.get("context")), {})
    return env, context


def seed_request(case, value):
    kind = interface(case)
    if kind == "json":
        return {"method": "POST", "content_type": "application/json", "body": json.dumps(value)}
    if kind == "query":
        return {"method": "GET", "query": value}
    return {"method": "GET", "params": {"input": value}}


def http_from_result(case, returncode, stdout, stderr, timed_out=False):
    """Map a fixture execution onto what a client would observe on the wire."""
    if timed_out:
        return 504, {"Content-Type": "text/plain"}, "Gateway Timeout\n"
    if returncode != 0:
        crashed = returncode < 0 or any(m in stderr for m in CRASH_MARKERS)
        # A reverse proxy reports a dead worker as 502; a handled failure is a 500.
        if crashed:
            return 502, {"Content-Type": "text/plain"}, "Bad Gateway\n"
        return 500, {"Content-Type": "text/plain"}, "Internal Server Error\n"
    lang = case["language"]
    if lang == "cgi":
        return cgi_response(json_text(stdout))
    if lang in STRUCTURED:
        try:
            value = json.loads(stdout)
        except ValueError:
            return 500, {"Content-Type": "text/plain"}, "Internal Server Error\n"
        return structured_response(value)
    text = stdout[:-1] if stdout.endswith("\n") else stdout
    return 200, {"Content-Type": "text/html; charset=utf-8"}, text


def json_text(stdout):
    try:
        value = json.loads(stdout)
    except ValueError:
        return stdout
    return value if isinstance(value, str) else json.dumps(value)


def structured_response(value):
    status = 200
    if isinstance(value, dict) and type(value.get("status")) is int and 100 <= value["status"] <= 599:
        status = value["status"]
        if set(value) == {"status", "body"}:
            value = value["body"]
    if isinstance(value, str):
        return status, {"Content-Type": "text/html; charset=utf-8"}, value
    return status, {"Content-Type": "application/json"}, json.dumps(value, sort_keys=True)


def cgi_response(text):
    """Parse CGI output (headers, blank line, body) the way a web server would."""
    for separator in ("\r\n\r\n", "\n\n"):
        head, found, body = text.partition(separator)
        if found:
            break
    else:
        return 200, {"Content-Type": "text/html; charset=utf-8"}, text
    status, headers = 200, {}
    raw_headers = []
    for line in head.replace("\r\n", "\n").split("\n"):
        name, colon, value = line.partition(":")
        if not colon:
            continue
        name, value = name.strip(), value.strip()
        if name.lower() == "status":
            try:
                status = int(value.split()[0])
            except (ValueError, IndexError):
                status = 500
        else:
            raw_headers.append((name, value))
    for name, value in raw_headers:
        headers[name] = value if name not in headers else headers[name] + ", " + value
    if "Location" in headers and status == 200:
        status = 302
    headers.setdefault("Content-Type", "text/html; charset=utf-8")
    return status, headers, body


class Target:
    def __init__(self, target_id, case, variant, build_root, work_root=None):
        self.id, self.case, self.variant = target_id, case, variant
        # Build location depends on the case, not the (random) id, so it can be cached.
        self.build = build_root / case["id"].replace("/", "__") / variant
        self.work_root = work_root or self.build
        self.command = None
        self.error = None
        ready = self.build / ".command.json"
        if ready.is_file():
            self.command = json.loads(ready.read_text())
        self.lock = threading.Lock()
        self.env, self.context = deployment(case)

    def ensure_built(self):
        with self.lock:
            if self.command is None and self.error is None:
                self.build.mkdir(parents=True, exist_ok=True)
                try:
                    self.command = prepare(self.case, self.variant, self.build)
                    (self.build / ".command.json").write_text(json.dumps(self.command))
                except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
                    self.error = str(exc)
        return self.error is None

    def execute(self, value, timeout):
        if not self.ensure_built():
            return 503, {"Content-Type": "text/plain"}, "Service Unavailable\n"
        structured = self.case["language"] in STRUCTURED
        if not structured and not isinstance(value, str):
            return 400, {"Content-Type": "text/plain"}, "Bad Request\n"
        if not structured and "\x00" in value:
            return 400, {"Content-Type": "text/plain"}, "Bad Request\n"
        arguments = self.command + [json.dumps(value) if structured else value]
        if self.case.get("oracle"):
            arguments += ["--oracle", self.case["oracle"], "--context", json.dumps(self.context)]
        self.work_root.mkdir(parents=True, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix="req-", dir=self.work_root))
        try:
            (work / "public").mkdir()
            (work / "public/welcome.txt").write_text("WELCOME")
            (work / "secret.txt").write_text("LAB_SECRET")
            (work / "private.txt").write_text("LAB_SECRET")
            try:
                result = process(arguments, work, timeout=timeout, env_overrides=self.env)
            except subprocess.TimeoutExpired:
                return http_from_result(self.case, 0, "", "", timed_out=True)
            return http_from_result(self.case, result.returncode, result.stdout, result.stderr)
        finally:
            shutil.rmtree(work, ignore_errors=True)


class Gateway:
    def __init__(self, cases, build_root, timeout=10, workers=4, named=False, work_root=None):
        self.timeout = timeout
        self.slots = threading.BoundedSemaphore(workers)
        self.named = named
        self.http_port = None
        self.proto_variant = "vulnerable"
        self.services = []
        variants = [(c, v) for c in cases for v in ("vulnerable", "fixed")]
        if not named:
            secrets.SystemRandom().shuffle(variants)
        self.targets = {}
        for case, variant in variants:
            # Named mode is for manual exploration; opaque ids keep scanners blind.
            target_id = case["id"] + "/" + variant if named else secrets.token_hex(8)
            self.targets[target_id] = Target(target_id, case, variant, build_root, work_root)

    def mapping(self):
        return {"schema_version": 1, "kind": "network",
                "targets": {t.id: {"case_id": t.case["id"], "variant": t.variant}
                            for t in self.targets.values()}}

    def discovery(self, base=""):
        items = []
        for t in self.targets.values():
            if t.error is not None:
                continue  # runtime missing or build failed: not served
            seeds = [seed_request(t.case, v["input"]) for v in t.case["tests"] if v["kind"] == "benign"]
            items.append({"id": t.id, "url": base + "/t/" + t.id, "interface": interface(t.case),
                          "seeds": seeds})
        return {"schema_version": 1, "targets": items}

    def status_report(self, http_port=None):
        from protoserve import SERVICE_SPECS
        running = {(name, tr): (port, srv) for name, port, tr, srv in self.services}
        port = http_port if http_port is not None else self.http_port
        services = [{
            "name": "http", "transport": "tcp", "port": port, "active": True,
            "variant": "both", "description": "HTTP gateway serving /t/<id>, /targets.json, /status.json",
        }]
        for name, tr, default_port, desc in SERVICE_SPECS:
            entry = running.get((name, tr))
            alive = entry is not None and entry[1].fileno() >= 0
            services.append({
                "name": name, "transport": tr,
                "port": entry[0] if entry is not None else default_port,
                "active": alive,
                "variant": self.proto_variant if alive else None,
                "description": desc,
            })
        active_targets = [t for t in self.targets.values() if t.error is None]
        inactive_targets = [t for t in self.targets.values() if t.error is not None]
        report = {
            "schema_version": 1,
            "mode": "named" if self.named else "blind",
            "services": services,
            "summary": {
                "active_services": sum(1 for s in services if s["active"]),
                "total_services": len(services),
                "active_targets": len(active_targets),
                "inactive_targets": len(inactive_targets),
                "total_targets": len(self.targets),
            },
        }
        if self.named:
            stacks = {}
            for lang in sorted(RUNTIMES):
                lang_targets = [t for t in self.targets.values() if t.case["language"] == lang]
                if not lang_targets:
                    continue
                ok = sum(1 for t in lang_targets if t.error is None)
                reasons = sorted({t.error for t in lang_targets if t.error is not None})
                stacks[lang] = {
                    "active": ok, "inactive": len(lang_targets) - ok,
                    "total": len(lang_targets), "status": "active" if ok else "inactive",
                    "reasons": reasons[:3],
                }
            report["stacks"] = stacks
            report["targets"] = [
                {
                    "id": t.id, "language": t.case["language"], "variant": t.variant,
                    "interface": interface(t.case), "active": t.error is None,
                    "reason": t.error,
                    "seed": seed_request(t.case, next(v["input"] for v in t.case["tests"] if v["kind"] == "benign")),
                }
                for t in self.targets.values()
            ]
        else:
            report["targets"] = [
                {"id": t.id, "interface": interface(t.case), "active": t.error is None}
                for t in active_targets
            ]
        return report

    def handle(self, target_id, value):
        target = self.targets.get(target_id)
        if target is None:
            return 404, {"Content-Type": "text/plain"}, "Not Found\n"
        with self.slots:
            return target.execute(value, self.timeout)

    def prebuild(self, log=print):
        missing_runtime = {}
        for index, t in enumerate(self.targets.values(), 1):
            lang = t.case["language"]
            missing = [x for x in RUNTIMES[lang] if not shutil.which(x)]
            if missing:
                t.error = "missing runtime: " + ", ".join(missing)
                missing_runtime[lang] = missing
                continue
            if not t.ensure_built():
                log("BUILD FAIL", t.id, t.error[-300:])
            if index % 50 == 0:
                log("built", index, "/", len(self.targets))
        return missing_runtime


def decode_input(target, method, query, body, content_type):
    """Translate an HTTP request into a fixture input according to the target interface."""
    kind = interface(target.case)
    if kind == "query":
        if method != "GET":
            raise ValueError("CGI targets accept GET")
        return query
    if kind == "json":
        if method != "POST":
            raise ValueError("JSON targets accept POST")
        return json.loads(body.decode("utf-8"))
    if method == "GET":
        values = parse_qs(query, keep_blank_values=True).get("input")
        if not values:
            raise ValueError("missing input parameter")
        return values[0]
    if content_type.startswith("application/x-www-form-urlencoded"):
        values = parse_qs(body.decode("utf-8"), keep_blank_values=True).get("input")
        if not values:
            raise ValueError("missing input parameter")
        return values[0]
    return body.decode("utf-8")


def render_dashboard(report):
    """Render a self-contained status page showing active/inactive services, stacks, and targets."""
    e = html.escape
    s = report["summary"]
    svc_rows = []
    for svc in report["services"]:
        badge = '<span class="badge ok">ACTIVE</span>' if svc["active"] else '<span class="badge off">INACTIVE</span>'
        variant = e(svc["variant"] or "-")
        svc_rows.append(
            f"<tr><td><strong>{e(svc['name'])}</strong></td>"
            f"<td>{svc['port'] or '-'}/{e(svc['transport'])}</td>"
            f"<td>{badge}</td><td>{variant}</td><td>{e(svc['description'])}</td></tr>"
        )
    stacks_html = ""
    if "stacks" in report:
        cards = []
        for lang, st in report["stacks"].items():
            cls = "ok" if st["active"] else "off"
            reason = f'<div class="muted">{e(st["reasons"][0])}</div>' if st["reasons"] else ""
            cards.append(
                f'<div class="stack {cls}"><strong>{e(lang)}</strong>'
                f'<span>{st["active"]}/{st["total"]}</span>{reason}</div>'
            )
        stacks_html = f'<section><h2>Stacks ({len(report["stacks"])})</h2><div class="stacks">{"".join(cards)}</div></section>'
    target_rows = []
    for t in report["targets"]:
        tid = e(t["id"])
        active = t["active"]
        badge = '<span class="badge ok">ACTIVE</span>' if active else '<span class="badge off">INACTIVE</span>'
        lang = e(t.get("language", ""))
        reason = e(t.get("reason") or "")
        seed_btn = ""
        if active and "seed" in t:
            seed_json = e(json.dumps(t["seed"]))
            seed_btn = f'<button type="button" onclick="probe(this)" data-id="{tid}" data-seed="{seed_json}">Test</button>'
        target_rows.append(
            f'<tr data-active="{"1" if active else "0"}" data-lang="{lang}">'
            f'<td><a href="/t/{tid}"><code>{tid}</code></a></td>'
            f'<td>{e(t["interface"])}</td><td>{badge}</td>'
            f'<td>{seed_btn} <span class="muted">{reason}</span></td></tr>'
        )
    lang_options = ""
    if "stacks" in report:
        lang_options = '<select id="langFilter" onchange="filterRows()"><option value="">All stacks</option>' + "".join(
            f'<option value="{e(l)}">{e(l)}</option>' for l in report["stacks"]
        ) + "</select>"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BADASS Network Status</title>
<style>
  :root {{ --bg:#0f172a; --card:#1e293b; --line:#334155; --fg:#e2e8f0; --muted:#94a3b8; --ok:#22c55e; --off:#ef4444; }}
  body {{ margin:0; font-family:system-ui,sans-serif; background:var(--bg); color:var(--fg); padding:24px; max-width:1180px; margin-inline:auto; }}
  h1,h2 {{ margin:0 0 12px; }} h2 {{ font-size:1.1rem; margin-top:26px; }}
  a {{ color:#38bdf8; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
  .top {{ display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between; margin-bottom:18px; }}
  .links {{ display:flex; gap:12px; font-size:.9rem; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin-bottom:18px; }}
  .card,.stack {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; }}
  .card .num {{ font-size:1.5rem; font-weight:700; margin-top:4px; }}
  .stacks {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }}
  .stack {{ display:flex; flex-direction:column; gap:2px; font-size:.9rem; border-left:4px solid var(--ok); }}
  .stack.off {{ border-left-color:var(--off); opacity:.8; }}
  table {{ width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line); border-radius:8px; overflow:hidden; font-size:.9rem; }}
  th,td {{ padding:8px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
  th {{ color:var(--muted); font-weight:600; }}
  .badge {{ display:inline-block; padding:2px 7px; border-radius:999px; font-size:.75rem; font-weight:700; }}
  .badge.ok {{ background:rgba(34,197,94,.16); color:#4ade80; }}
  .badge.off {{ background:rgba(239,68,68,.16); color:#f87171; }}
  .muted {{ color:var(--muted); font-size:.82rem; }}
  .controls {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px; }}
  input,select,button {{ background:var(--card); color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:6px 10px; font-size:.9rem; }}
  button {{ cursor:pointer; }} button:hover {{ border-color:#38bdf8; }}
  pre {{ background:#020617; border:1px solid var(--line); border-radius:8px; padding:10px; overflow:auto; max-height:180px; display:none; }}
</style></head><body>
<div class="top">
  <div><h1>BADASS Network Lab</h1><div class="muted">Mode: {e(report['mode'])} &middot; <button type="button" onclick="location.reload()">Refresh</button></div></div>
  <div class="links"><a href="/status.json">status.json</a><a href="/services.json">services.json</a><a href="/targets.json">targets.json</a></div>
</div>
<div class="cards">
  <div class="card"><div class="muted">Network Services</div><div class="num">{s['active_services']} / {s['total_services']}</div></div>
  <div class="card"><div class="muted">Active Targets</div><div class="num">{s['active_targets']} / {s['total_targets']}</div></div>
  <div class="card"><div class="muted">Inactive Targets</div><div class="num">{s['inactive_targets']}</div></div>
</div>
<section><h2>Network Services</h2>
  <table><thead><tr><th>Service</th><th>Port</th><th>Status</th><th>Variant</th><th>Details</th></tr></thead>
  <tbody>{''.join(svc_rows)}</tbody></table>
</section>
{stacks_html}
<section><h2>Targets</h2>
  <div class="controls">
    <input id="q" type="search" placeholder="Filter targets..." oninput="filterRows()">
    <select id="stateFilter" onchange="filterRows()"><option value="">All states</option><option value="1">Active only</option><option value="0">Inactive only</option></select>
    {lang_options}
  </div>
  <pre id="probeOut"></pre>
  <table><thead><tr><th>Target</th><th>Interface</th><th>Status</th><th>Action / Notes</th></tr></thead>
  <tbody id="targetRows">{''.join(target_rows)}</tbody></table>
</section>
<script>
function filterRows() {{
  const q = document.getElementById('q').value.toLowerCase();
  const st = document.getElementById('stateFilter').value;
  const lf = document.getElementById('langFilter');
  const lang = lf ? lf.value : '';
  for (const row of document.querySelectorAll('#targetRows tr')) {{
    const okQ = !q || row.textContent.toLowerCase().includes(q);
    const okS = !st || row.dataset.active === st;
    const okL = !lang || row.dataset.lang === lang;
    row.style.display = (okQ && okS && okL) ? '' : 'none';
  }}
}}
async function probe(btn) {{
  const seed = JSON.parse(btn.dataset.seed);
  let url = '/t/' + btn.dataset.id;
  const opts = {{ method: seed.method || 'GET', headers: {{}} }};
  if (seed.content_type) opts.headers['Content-Type'] = seed.content_type;
  if (seed.body !== undefined) opts.body = seed.body;
  if (seed.query !== undefined) url += '?' + seed.query;
  if (seed.params && seed.params.input !== undefined) url += '?input=' + encodeURIComponent(seed.params.input);
  const res = await fetch(url, opts);
  const text = await res.text();
  const out = document.getElementById('probeOut');
  out.style.display = 'block';
  out.textContent = seed.method + ' ' + url + ' -> HTTP ' + res.status + '\\n' + text;
}}
</script></body></html>"""


def make_handler(gateway):
    class Handler(BaseHTTPRequestHandler):
        server_version = "badass-gateway"
        sys_version = ""

        def log_message(self, fmt, *args):
            if os.environ.get("BADASS_NET_ACCESS_LOG"):
                sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

        def send(self, status, headers, body):
            data = body.encode("utf-8", "replace")
            self.send_response(status)
            for name, value in headers.items():
                # Emit fixture headers verbatim but never let them break framing.
                safe = value.replace("\r", "%0D").replace("\n", "%0A")
                self.send_header(name, safe)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)

        def route(self, method):
            parts = urlsplit(self.path)
            if method == "GET" and parts.path == "/status.json":
                port = self.server.server_address[1] if getattr(self, "server", None) else None
                return self.send(200, {"Content-Type": "application/json"},
                                 json.dumps(gateway.status_report(port)))
            if method == "GET" and parts.path == "/services.json":
                doc = {"schema_version": 1, "services": [
                    {"name": name, "port": port, "transport": transport}
                    for name, port, transport, _ in gateway.services
                ]}
                return self.send(200, {"Content-Type": "application/json"}, json.dumps(doc))
            if method == "GET" and parts.path == "/":
                port = self.server.server_address[1] if getattr(self, "server", None) else None
                return self.send(200, {"Content-Type": "text/html; charset=utf-8"},
                                 render_dashboard(gateway.status_report(port)))
            if method == "GET" and parts.path == "/targets.json":
                return self.send(200, {"Content-Type": "application/json"},
                                 json.dumps(gateway.discovery()))
            if not parts.path.startswith("/t/"):
                return self.send(404, {"Content-Type": "text/plain"}, "Not Found\n")
            target_id = parts.path[3:]
            target = gateway.targets.get(target_id)
            if target is None:
                return self.send(404, {"Content-Type": "text/plain"}, "Not Found\n")
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                return self.send(400, {"Content-Type": "text/plain"}, "Bad Request\n")
            if length < 0:
                return self.send(400, {"Content-Type": "text/plain"}, "Bad Request\n")
            if length > MAX_BODY:
                return self.send(413, {"Content-Type": "text/plain"}, "Payload Too Large\n")
            body = self.rfile.read(length) if length else b""
            try:
                value = decode_input(target, method, parts.query, body,
                                     self.headers.get("Content-Type", ""))
            except (ValueError, UnicodeDecodeError):
                return self.send(400, {"Content-Type": "text/plain"}, "Bad Request\n")
            return self.send(*gateway.handle(target_id, value))

        def do_GET(self):
            self.route("GET")

        def do_POST(self):
            self.route("POST")

    return Handler


def observability(gateway, log=print):
    """Upper bound for any network-only detector: does an attack change the wire response?"""
    by_case = {}
    for t in gateway.targets.values():
        by_case.setdefault(t.case["id"], {})[t.variant] = t
    rows = []
    for case_id, pair in sorted(by_case.items()):
        case = pair["vulnerable"].case
        differing = []
        for vector in case["tests"]:
            if vector["kind"] != "attack":
                continue
            responses = [pair[v].execute(vector["input"], gateway.timeout) for v in ("vulnerable", "fixed")]
            if responses[0] != responses[1]:
                differing.append(vector["name"])
        unavailable = any(pair[v].error for v in pair)
        rows.append({"case_id": case_id, "cwe": case["cwe"], "network_observable": bool(differing),
                     "unavailable": unavailable, "differing_vectors": differing})
        log(("OBSERVABLE " if differing else ("UNAVAILABLE " if unavailable else "HIDDEN ")) + case_id)
    available = [r for r in rows if not r["unavailable"]]
    return {"cases": len(rows), "available": len(available),
            "network_observable": sum(r["network_observable"] for r in available),
            "note": "A case is observable when an attack vector yields a different HTTP status, headers "
                    "or body between variants. File-system-only effects are invisible from the network.",
            "results": rows}


def select(args):
    cases = read_catalog()
    validate(cases)
    cases = [c for c in cases if (not args.language or c["language"] in args.language)
             and (not args.cwe or args.cwe in c["cwe"]) and (not args.case or c["id"] == args.case)]
    if not cases:
        raise SystemExit("No matching cases")
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["serve", "observability", "build"], nargs="?", default="serve")
    parser.add_argument("--build-dir", type=Path,
                        help="Persistent compilation cache (precompiled into the Docker image)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8808)
    parser.add_argument("--language", action="append", choices=sorted(RUNTIMES))
    parser.add_argument("--cwe")
    parser.add_argument("--case")
    parser.add_argument("--mapping", type=Path, help="Private answer key (serve mode); keep it away from scanners")
    parser.add_argument("--output", type=Path, help="Observability report path")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--lazy", action="store_true", help="Compile on first request instead of at startup")
    parser.add_argument("--named", action="store_true",
                        help="Readable routes /t/<language>/<case>/<variant> instead of opaque ids")
    parser.add_argument("--services", action="store_true",
                        help="Also start non-HTTP protocol listeners (HTTPS, FTP, Telnet, SMTP, LDAP, DNS, RESP, TCP)")
    parser.add_argument("--proto-variant", choices=["vulnerable", "fixed"], default="vulnerable",
                        help="Default variant used by non-HTTP protocol services")
    args = parser.parse_args(argv)
    cases = select(args)
    (ROOT / ".build").mkdir(exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="net-", dir=ROOT / ".build"))
    build_root = args.build_dir.resolve() if args.build_dir else scratch / "build"
    gateway = Gateway(cases, build_root, args.timeout, args.workers, args.named, scratch / "work")
    try:
        if args.command == "build":
            missing = gateway.prebuild()
            failed = [t.case["id"] + "/" + t.variant for t in gateway.targets.values()
                      if t.error and not t.error.startswith("missing runtime")]
            built = sum(1 for t in gateway.targets.values() if t.error is None)
            print(json.dumps({"built": built, "total": len(gateway.targets), "failed": failed,
                              "missing_runtimes": missing}))
            return int(bool(failed))
        if args.command == "observability":
            gateway.prebuild()
            report = observability(gateway)
            text = json.dumps(report, indent=2) + "\n"
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(text)
                print("Report:", args.output)
            print(json.dumps({k: report[k] for k in ("cases", "available", "network_observable")}))
            return 0
        if not args.mapping and not args.named:
            parser.error("serve requires --mapping (private answer key) unless --named is used")
        if args.mapping:
            if args.mapping.exists():
                parser.error("Choose a new mapping path; ids are regenerated on every start")
            args.mapping.parent.mkdir(parents=True, exist_ok=True)
            with args.mapping.open("x", encoding="utf-8") as stream:
                json.dump(gateway.mapping(), stream, indent=2, sort_keys=True)
        if not args.lazy:
            missing = gateway.prebuild()
            for lang, tools in sorted(missing.items()):
                print("SKIP", lang, "missing:", ", ".join(tools), file=sys.stderr)
        gateway.http_port = args.port
        gateway.proto_variant = args.proto_variant
        server = ThreadingHTTPServer((args.host, args.port), make_handler(gateway))
        if args.services:
            from protoserve import start_services
            gateway.services = start_services(
                gateway, args.host, variant=args.proto_variant,
                tls_dir=scratch / "tls", https_handler_factory=make_handler,
            )
            for name, port, transport, _ in gateway.services:
                print("Service %-6s %s://%s:%d/" % (name, transport, args.host, port), flush=True)
        available = sum(1 for t in gateway.targets.values() if t.error is None)
        print("Serving %d/%d targets on http://%s:%d/ (%s)" % (
            available, len(gateway.targets), args.host, args.port,
            "named routes" if args.named else "mapping: %s" % args.mapping), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            for _, _, _, srv in gateway.services:
                srv.shutdown()
                srv.server_close()
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

