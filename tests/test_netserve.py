from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import socket
import ssl
import struct
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lab import read_catalog  # noqa: E402
from netserve import Gateway, cgi_response, http_from_result, make_handler, observability  # noqa: E402
from protoserve import _ber_tlv, start_services  # noqa: E402


class NetserveTests(unittest.TestCase):
    def setUp(self):
        cases = {c["id"]: c for c in read_catalog()}
        self.cases = [
            cases["rest-api/xss"],
            cases["cgi/header-injection"],
            cases["python/path-traversal"],
        ]

    def test_named_gateway_serves_discovery_and_distinguishes_variants(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gateway = Gateway(self.cases, root / "build", named=True, work_root=root / "work")
            gateway.prebuild(log=lambda *_: None)
            server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(gateway))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_address[1]}"
                with urllib.request.urlopen(base + "/targets.json", timeout=5) as resp:
                    doc = json.loads(resp.read().decode())
                ids = {item["id"] for item in doc["targets"]}
                self.assertEqual(len(ids), 6)
                self.assertIn("rest-api/xss/vulnerable", ids)
                self.assertIn("rest-api/xss/fixed", ids)
                self.assertNotIn("cwe", json.dumps(doc).lower())

                for variant, expected in (("vulnerable", "<p><b>hi</b></p>"),
                                          ("fixed", "<p>&lt;b&gt;hi&lt;/b&gt;</p>")):
                    req = urllib.request.Request(
                        f"{base}/t/rest-api/xss/{variant}",
                        data=json.dumps({"value": "<b>hi</b>"}).encode(),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        self.assertEqual(resp.status, 200)
                        self.assertEqual(resp.read().decode(), expected)

                class NoRedirect(urllib.request.HTTPRedirectHandler):
                    def redirect_request(self, req, fp, code, msg, headers, newurl):
                        return None

                opener = urllib.request.build_opener(NoRedirect)
                with self.assertRaises(urllib.error.HTTPError) as ctx:
                    opener.open(f"{base}/t/cgi/header-injection/vulnerable?/home", timeout=5)
                self.assertEqual(ctx.exception.code, 302)
                self.assertEqual(ctx.exception.headers["Location"], "/home")
                ctx.exception.close()

                with self.assertRaises(urllib.error.HTTPError) as bad_len:
                    req = urllib.request.Request(
                        f"{base}/t/rest-api/xss/fixed",
                        data=b"{}",
                        headers={"Content-Length": "-1"},
                        method="POST",
                    )
                    urllib.request.urlopen(req, timeout=5)
                self.assertEqual(bad_len.exception.code, 400)
                bad_len.exception.close()
            finally:
                server.shutdown()
                server.server_close()

    def test_blind_mode_hides_names_and_builds_complete_mapping(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gateway = Gateway(self.cases[:1], root / "build", named=False, work_root=root / "work")
            gateway.prebuild(log=lambda *_: None)
            mapping = gateway.mapping()
            discovery = gateway.discovery()
            self.assertEqual(len(mapping["targets"]), 2)
            self.assertEqual(len(discovery["targets"]), 2)
            for item in discovery["targets"]:
                self.assertNotIn("xss", item["id"])
                self.assertIn(item["id"], mapping["targets"])
                self.assertEqual(mapping["targets"][item["id"]]["case_id"], "rest-api/xss")
            self.assertEqual({v["variant"] for v in mapping["targets"].values()}, {"vulnerable", "fixed"})
            status = gateway.status_report(8808)
            self.assertEqual(status["mode"], "blind")
            self.assertNotIn("stacks", status)
            self.assertNotIn("xss", json.dumps(status).lower())

    def test_dashboard_and_status_report_show_active_and_inactive(self):
        cases = {c["id"]: c for c in read_catalog()}
        mixed = [cases["rest-api/xss"], cases["go/xss"]]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gateway = Gateway(mixed, root / "build", named=True, work_root=root / "work")
            gateway.prebuild(log=lambda *_: None)
            gateway.targets["go/xss/fixed"].error = "missing runtime: go"
            gateway.targets["go/xss/vulnerable"].error = "missing runtime: go"
            server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(gateway))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_address[1]}"
                with urllib.request.urlopen(base + "/status.json", timeout=5) as resp:
                    status = json.loads(resp.read().decode())
                self.assertEqual(status["summary"]["active_services"], 1)
                self.assertEqual(status["summary"]["total_services"], 10)
                self.assertEqual(status["summary"]["active_targets"], 2)
                self.assertEqual(status["summary"]["inactive_targets"], 2)
                self.assertEqual(status["stacks"]["rest-api"]["status"], "active")
                self.assertEqual(status["stacks"]["go"]["status"], "inactive")

                with urllib.request.urlopen(base + "/", timeout=5) as resp:
                    page = resp.read().decode()
                self.assertIn("BADASS Network Lab", page)
                self.assertIn("ACTIVE", page)
                self.assertIn("INACTIVE", page)
                self.assertIn("rest-api/xss/vulnerable", page)
                self.assertIn("missing runtime: go", page)
            finally:
                server.shutdown()
                server.server_close()

    def test_build_cache_reuses_command_across_gateways(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            build_dir = root / "cache"
            g1 = Gateway(self.cases[:1], build_dir, named=True, work_root=root / "w1")
            g1.prebuild(log=lambda *_: None)
            cmd_file = build_dir / "rest-api__xss" / "vulnerable" / ".command.json"
            self.assertTrue(cmd_file.is_file())
            g2 = Gateway(self.cases[:1], build_dir, named=False, work_root=root / "w2")
            self.assertTrue(all(t.command is not None for t in g2.targets.values()))

    def test_http_mapping_and_observability(self):
        self.assertEqual(http_from_result({"language": "c"}, -11, "", "Segmentation fault")[0], 502)
        self.assertEqual(http_from_result({"language": "c"}, 1, "", "error")[0], 500)
        self.assertEqual(http_from_result({"language": "c"}, 0, "", "", timed_out=True)[0], 504)
        status, headers, body = cgi_response("Status: 400 Bad Request\r\nX-Test: a\r\n\r\nDENIED")
        self.assertEqual((status, headers["X-Test"], body), (400, "a", "DENIED"))

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gateway = Gateway(self.cases, root / "build", named=True, work_root=root / "work")
            gateway.prebuild(log=lambda *_: None)
            report = observability(gateway, log=lambda *_: None)
            self.assertEqual(report["cases"], 3)
            self.assertEqual(report["network_observable"], 3)

    def test_multi_protocol_services_expose_non_http_vulnerabilities(self):
        cases = {c["id"]: c for c in read_catalog()}
        selected = [
            cases["rest-api/xss"],
            cases["python/path-traversal"],
            cases["python/hardcoded-credentials"],
            cases["python/command-injection"],
            cases["python/jenkins-cli-atfile"],
            cases["python/error-disclosure"],
            cases["python/log-injection"],
            cases["python/header-injection"],
            cases["python/gitlab-reset-recipients"],
            cases["python/ldap-injection"],
            cases["python/code-injection"],
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gateway = Gateway(selected, root / "build", named=True, work_root=root / "work")
            gateway.prebuild(log=lambda *_: None)
            ephemeral = {k: 0 for k in ("https", "ftp", "ftp_data", "telnet", "smtp", "ldap", "dns", "resp", "tcp")}
            services = start_services(
                gateway, "127.0.0.1", ports=ephemeral, variant="vulnerable",
                tls_dir=root / "tls", https_handler_factory=make_handler,
            )
            ports = {(name, tr): port for name, port, tr, _ in services}
            try:
                # 1. HTTPS (including resilience to non-TLS probes)
                with socket.create_connection(("127.0.0.1", ports[("https", "tcp")]), timeout=5) as raw:
                    raw.sendall(b"GET / HTTP/1.0\r\n\r\n")
                ctx = ssl._create_unverified_context()
                with urllib.request.urlopen(
                    f"https://127.0.0.1:{ports[('https', 'tcp')]}/targets.json", context=ctx, timeout=5
                ) as resp:
                    self.assertEqual(len(json.loads(resp.read().decode())["targets"]), len(selected) * 2)

                # 2. Raw TCP gateway
                with socket.create_connection(("127.0.0.1", ports[("tcp", "tcp")]), timeout=5) as s:
                    banner = s.recv(1024).decode()
                    self.assertIn("BADASS-TCP", banner)
                    s.sendall(b'RUN rest-api/xss/vulnerable {"value":"<i>x</i>"}\n')
                    reply = s.recv(4096).decode()
                    self.assertIn("<p><i>x</i></p>", reply)

                # 3. FTP anonymous + path traversal
                with socket.create_connection(("127.0.0.1", ports[("ftp", "tcp")]), timeout=5) as s:
                    f = s.makefile("rw", encoding="utf-8", newline="\r\n")
                    self.assertTrue(f.readline().startswith("220"))
                    f.write("USER anonymous\r\n"); f.flush()
                    self.assertTrue(f.readline().startswith("331"))
                    f.write("PASS x\r\n"); f.flush()
                    self.assertTrue(f.readline().startswith("230"))
                    f.write("EPSV\r\n"); f.flush()
                    epsv = f.readline()
                    self.assertTrue(epsv.startswith("229"))
                    data_port = int(epsv.split("|||")[1].split("|")[0])
                    with socket.create_connection(("127.0.0.1", data_port), timeout=5) as ds:
                        f.write("RETR ../secret.txt\r\n"); f.flush()
                        self.assertTrue(f.readline().startswith("150"))
                        self.assertEqual(ds.recv(1024).decode(), "LAB_SECRET")
                    self.assertTrue(f.readline().startswith("226"))

                # 4. Telnet CLI (hardcoded password + @file + mode fixed)
                def recv_until(sock, marker):
                    buf = ""
                    while marker not in buf:
                        chunk = sock.recv(4096)
                        if not chunk:
                            break
                        buf += chunk.decode()
                    return buf

                with socket.create_connection(("127.0.0.1", ports[("telnet", "tcp")]), timeout=5) as s:
                    recv_until(s, "Password: ")
                    s.sendall(b"BADASS_LAB_DEFAULT\n")
                    self.assertIn("Welcome", recv_until(s, "admin> "))
                    s.sendall(b"help @secret.txt\n")
                    self.assertIn("LAB_SECRET", recv_until(s, "admin> "))
                    s.sendall(b"mode fixed\n")
                    self.assertIn("Mode: fixed", recv_until(s, "admin> "))
                    s.sendall(b"status\n")
                    self.assertIn("Service unavailable", recv_until(s, "admin> "))

                # 5. SMTP VRFY enumeration
                with socket.create_connection(("127.0.0.1", ports[("smtp", "tcp")]), timeout=5) as s:
                    f = s.makefile("rw", encoding="utf-8", newline="\r\n")
                    self.assertTrue(f.readline().startswith("220"))
                    f.write("VRFY alice\r\n"); f.flush()
                    self.assertIn("alice@example.test", f.readline())

                # 6. LDAPv3 BER SearchRequest injection
                with socket.create_connection(("127.0.0.1", ports[("ldap", "tcp")]), timeout=5) as s:
                    bind_req = _ber_tlv(0x30, _ber_tlv(0x02, b"\x01") + _ber_tlv(
                        0x60, _ber_tlv(0x02, b"\x03") + _ber_tlv(0x04, b"") + _ber_tlv(0x80, b"")
                    ))
                    s.sendall(bind_req)
                    self.assertIn(b"\x61", s.recv(1024))
                    flt = _ber_tlv(0xA3, _ber_tlv(0x04, b"uid") + _ber_tlv(0x04, b"admin)(|(uid=*"))
                    srch = (
                        _ber_tlv(0x04, b"dc=badass,dc=local") + _ber_tlv(0x0A, b"\x02")
                        + _ber_tlv(0x0A, b"\x00") + _ber_tlv(0x02, b"\x00")
                        + _ber_tlv(0x02, b"\x00") + _ber_tlv(0x01, b"\x00")
                        + flt + _ber_tlv(0x30, b"")
                    )
                    s.sendall(_ber_tlv(0x30, _ber_tlv(0x02, b"\x02") + _ber_tlv(0x63, srch)))
                    data = s.recv(4096)
                    self.assertIn(b"secret-admin@example.test", data)

                # 7. DNS rebinding (UDP)
                def dns_query(name, qtype=1):
                    qname = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00"
                    pkt = struct.pack("!HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0) + qname + struct.pack("!HH", qtype, 1)
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as us:
                        us.settimeout(5)
                        us.sendto(pkt, ("127.0.0.1", ports[("dns", "udp")]))
                        return us.recv(1024)

                r1 = dns_query("rebind.badass.local", 1)
                r2 = dns_query("rebind.badass.local", 1)
                self.assertEqual(socket.inet_ntoa(r1[-4:]), "93.184.216.34")
                self.assertEqual(socket.inet_ntoa(r2[-4:]), "127.0.0.1")
                r_txt = dns_query("secret.badass.local", 16)
                self.assertIn(b"LAB_SECRET", r_txt)

                # 8. RESP (Redis-like) unauthenticated INFO + EVAL + malformed probe resilience
                with socket.create_connection(("127.0.0.1", ports[("resp", "tcp")]), timeout=5) as bad:
                    bad.sendall(b"*bad\r\n")
                with socket.create_connection(("127.0.0.1", ports[("resp", "tcp")]), timeout=5) as s:
                    s.sendall(b"*1\r\n$4\r\nINFO\r\n")
                    self.assertIn(b"LAB_SECRET", s.recv(4096))
                    s.sendall(b"*2\r\n$4\r\nEVAL\r\n$3\r\n2+3\r\n")
                    self.assertIn(b"\r\n5\r\n", s.recv(1024))
            finally:
                for _, _, _, srv in services:
                    srv.shutdown()
                    srv.server_close()


if __name__ == "__main__":
    unittest.main()
