#!/usr/bin/env python3
"""Multi-protocol network service listeners backed by BADASS fixtures.

Exposes non-HTTP services alongside the HTTP gateway in tools/netserve.py so
network scanners and protocol clients see realistic LAN targets:
  * HTTPS (TLS)     8443/tcp  same HTTP gateway over TLS (self-signed cert)
  * FTP             2121/tcp  (data 2122/tcp) anonymous/hardcoded login + RETR traversal
  * Telnet / CLI    2323/tcp  hardcoded auth, command injection, @file expansion
  * SMTP            2525/tcp  header/log injection, VRFY user enum, multi-recipient reset
  * LDAPv3          3389/tcp  ASN.1/BER Bind + Search backed by python/ldap-injection
  * DNS             5353/udp+tcp  DNS rebinding (rebind.badass.local) + TXT disclosure
  * RESP (Redis)    6379/tcp  unauthenticated INFO disclosure + EVAL code injection
  * Raw TCP         9001/tcp  line gateway to execute any catalog target over TCP
"""
import ipaddress
import json
from pathlib import Path
import socket
import socketserver
import ssl
import struct
import subprocess
import threading


DEFAULT_PORTS = {
    "https": 8443,
    "ftp": 2121,
    "ftp_data": 2122,
    "telnet": 2323,
    "smtp": 2525,
    "ldap": 3389,
    "dns": 5353,
    "resp": 6379,
    "tcp": 9001,
}

SERVICE_SPECS = [
    ("https", "tcp", DEFAULT_PORTS["https"], "TLS gateway (self-signed cert) serving /t/<id>"),
    ("ftp", "tcp", DEFAULT_PORTS["ftp"], "Anonymous/default login (CWE-798), RETR traversal (CWE-22)"),
    ("telnet", "tcp", DEFAULT_PORTS["telnet"], "Admin CLI: default auth, ping injection (CWE-78), @file (CWE-73)"),
    ("smtp", "tcp", DEFAULT_PORTS["smtp"], "VRFY enum, header/log injection (CWE-113/117), reset recipients"),
    ("ldap", "tcp", DEFAULT_PORTS["ldap"], "LDAPv3 ASN.1/BER search filter injection (CWE-90)"),
    ("dns", "udp", DEFAULT_PORTS["dns"], "DNS rebinding on rebind.badass.local & TXT disclosure"),
    ("dns", "tcp", DEFAULT_PORTS["dns"], "DNS over TCP (same records as UDP)"),
    ("resp", "tcp", DEFAULT_PORTS["resp"], "Redis-like RESP2: unauth INFO (CWE-209) & EVAL (CWE-95)"),
    ("tcp", "tcp", DEFAULT_PORTS["tcp"], "Raw TCP line gateway (LIST | RUN <target_id> <input>)"),
]


class Resolver:
    """Lookup backing catalog targets by (case_id, variant) regardless of opaque ids."""

    def __init__(self, gateway, default_variant="vulnerable"):
        self.gateway = gateway
        self.default_variant = default_variant
        self.by_case = {(t.case["id"], t.variant): t for t in gateway.targets.values()}

    def run(self, case_id, value, variant=None):
        target = self.by_case.get((case_id, variant or self.default_variant))
        if target is None:
            return None
        return target.execute(value, self.gateway.timeout)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        import sys
        exc = sys.exc_info()[1]
        if isinstance(exc, (BrokenPipeError, ConnectionResetError, TimeoutError, socket.timeout, ssl.SSLError)):
            return
        super().handle_error(request, client_address)


def make_tls_http_server(address, handler_class, ssl_context):
    from http.server import ThreadingHTTPServer

    class TLSHTTPServer(ThreadingHTTPServer):
        allow_reuse_address = True
        daemon_threads = True

        def process_request_thread(self, request, client_address):
            # Perform TLS handshake in the worker thread so non-TLS probes cannot stall accept().
            try:
                request.settimeout(5)
                request.do_handshake()
                request.settimeout(None)
            except (ssl.SSLError, OSError, TimeoutError):
                self.shutdown_request(request)
                return
            super().process_request_thread(request, client_address)

        def handle_error(self, request, client_address):
            import sys
            exc = sys.exc_info()[1]
            if isinstance(exc, (BrokenPipeError, ConnectionResetError, TimeoutError, socket.timeout, ssl.SSLError)):
                return
            super().handle_error(request, client_address)

    srv = TLSHTTPServer(address, handler_class)
    srv.socket = ssl_context.wrap_socket(srv.socket, server_side=True, do_handshake_on_connect=False)
    return srv


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    allow_reuse_address = True
    daemon_threads = True


def _readline(sock, limit=8192):
    buf = bytearray()
    while len(buf) < limit:
        chunk = sock.recv(1)
        if not chunk:
            break
        buf.extend(chunk)
        if chunk == b"\n":
            break
    if not buf:
        return None
    return buf.decode("utf-8", "replace").rstrip("\r\n")


def generate_tls_cert(cert_dir):
    """Create a self-signed certificate for the HTTPS listener."""
    cert_dir.mkdir(parents=True, exist_ok=True)
    cert = cert_dir / "cert.pem"
    key = cert_dir / "key.pem"
    if not (cert.is_file() and key.is_file()):
        subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", str(key), "-out", str(cert), "-days", "7",
                "-subj", "/CN=badass.local",
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
    return cert, key


# --------------------------------------------------------------------------- Raw TCP (9001)
def make_tcp_handler(gateway):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            self.request.sendall(b"220 BADASS-TCP 1.0 (LIST | RUN <target_id> <input> | QUIT)\r\n")
            while True:
                line = _readline(self.request)
                if line is None:
                    break
                cmd = line.strip()
                if not cmd:
                    continue
                upper = cmd.upper()
                if upper == "QUIT":
                    self.request.sendall(b"221 Bye\r\n")
                    break
                if upper == "LIST":
                    doc = gateway.discovery()
                    lines = "".join(f"{t['id']} {t['interface']}\n" for t in doc["targets"])
                    self.request.sendall((lines + ".\r\n").encode())
                    continue
                if upper.startswith("RUN "):
                    rest = cmd[4:].strip()
                    parts = rest.split(" ", 1)
                    target_id = parts[0]
                    raw_val = parts[1] if len(parts) > 1 else ""
                    target = gateway.targets.get(target_id)
                    if target is None:
                        self.request.sendall(b"ERR 404 Not Found\r\n")
                        continue
                    value = raw_val
                    if target.case["language"] in {"python", "cgi", "rest-api", "ai"}:
                        try:
                            value = json.loads(raw_val) if raw_val else ""
                        except ValueError:
                            value = raw_val
                    status, _headers, body = gateway.handle(target_id, value)
                    if status == 502:
                        self.request.sendall(b"ERR 502 Bad Gateway (target crashed)\r\n")
                        break
                    if status >= 400:
                        self.request.sendall(f"ERR {status} {body.strip()}\r\n".encode())
                        continue
                    data = body.encode("utf-8", "replace")
                    self.request.sendall(f"OK {len(data)}\r\n".encode() + data + b"\r\n")
                    continue
                self.request.sendall(b"ERR 400 Unknown command\r\n")

    return Handler


# --------------------------------------------------------------------------- FTP (2121 / 2122)
def make_ftp_handler(resolver, data_port_box):
    data_lock = threading.Lock()

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            variant = resolver.default_variant
            user = None
            authed = False
            data_listener = None

            def send(msg):
                self.request.sendall((msg + "\r\n").encode())

            def close_data():
                nonlocal data_listener
                if data_listener is not None:
                    try:
                        data_listener.close()
                    except OSError:
                        pass
                    data_listener = None

            send("220 badass-ftp.local FTP server ready")
            try:
                while True:
                    line = _readline(self.request)
                    if line is None:
                        break
                    verb, _, arg = line.partition(" ")
                    cmd = verb.upper()
                    arg = arg.strip()
                    if cmd == "USER":
                        user = arg
                        if user == "fixed":
                            variant = "fixed"
                        elif user == "vulnerable":
                            variant = "vulnerable"
                        send("331 Password required for " + (user or "user"))
                    elif cmd == "PASS":
                        if variant == "vulnerable" and user in {"anonymous", "ftp"}:
                            authed = True
                            send("230 Anonymous login ok")
                            continue
                        res = resolver.run("python/hardcoded-credentials", arg, variant=variant)
                        if res and res[0] == 200 and res[2] == "ADMIN":
                            authed = True
                            send("230 Login successful")
                        else:
                            authed = False
                            send("530 Login incorrect")
                    elif cmd == "QUIT":
                        send("221 Goodbye")
                        break
                    elif cmd == "NOOP":
                        send("200 OK")
                    elif cmd == "SYST":
                        send("215 UNIX Type: L8")
                    elif cmd == "FEAT":
                        send("211-Features:\r\n PASV\r\n EPSV\r\n SIZE\r\n211 End")
                    elif cmd == "PWD":
                        send('257 "/" is current directory')
                    elif cmd == "TYPE":
                        send("200 Type set to " + (arg or "I"))
                    elif cmd in {"PASV", "EPSV"}:
                        if not authed:
                            send("530 Please login with USER and PASS")
                            continue
                        close_data()
                        try:
                            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            srv.bind(("0.0.0.0", data_port_box[0]))
                            srv.listen(1)
                            srv.settimeout(10)
                            data_listener = srv
                            actual_port = srv.getsockname()[1]
                            if cmd == "EPSV":
                                send(f"229 Entering Extended Passive Mode (|||{actual_port}|)")
                            else:
                                ip = self.request.getsockname()[0].replace(".", ",")
                                send(f"227 Entering Passive Mode ({ip},{actual_port >> 8},{actual_port & 255})")
                        except OSError:
                            send("425 Can't open passive connection")
                    elif cmd in {"LIST", "NLST"}:
                        if not authed:
                            send("530 Not logged in")
                            continue
                        if data_listener is None:
                            send("425 Use PASV or EPSV first")
                            continue
                        with data_lock:
                            send("150 Opening data connection")
                            conn, _ = data_listener.accept()
                            try:
                                listing = "welcome.txt\r\n" if cmd == "NLST" else "-rw-r--r-- 1 lab lab 7 welcome.txt\r\n"
                                conn.sendall(listing.encode())
                            finally:
                                conn.close()
                                close_data()
                        send("226 Transfer complete")
                    elif cmd == "RETR":
                        if not authed:
                            send("530 Not logged in")
                            continue
                        res = resolver.run("python/path-traversal", arg.lstrip("/"), variant=variant)
                        if not res or res[0] != 200 or res[2] == "DENIED":
                            close_data()
                            send("550 File unavailable or access denied")
                            continue
                        if data_listener is None:
                            send("425 Use PASV or EPSV first")
                            continue
                        with data_lock:
                            send("150 Opening data connection")
                            conn, _ = data_listener.accept()
                            try:
                                conn.sendall(res[2].encode("utf-8", "replace"))
                            finally:
                                conn.close()
                                close_data()
                        send("226 Transfer complete")
                    else:
                        send("502 Command not implemented")
            finally:
                close_data()

    return Handler


# --------------------------------------------------------------------------- Telnet / Admin CLI (2323)
def make_telnet_handler(resolver):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            variant = resolver.default_variant
            self.request.sendall(b"BADASS Admin CLI v1.0\r\nPassword: ")
            pw = _readline(self.request)
            if pw is None:
                return
            auth = resolver.run("python/hardcoded-credentials", pw, variant=variant)
            if not (auth and auth[0] == 200 and auth[2] == "ADMIN"):
                self.request.sendall(b"Authentication failed.\r\n")
                return
            self.request.sendall(
                b"Welcome. Commands: ping <host> | help <arg> | status | mode <vulnerable|fixed> | quit\r\nadmin> "
            )
            while True:
                line = _readline(self.request)
                if line is None:
                    break
                cmd = line.strip()
                if not cmd:
                    self.request.sendall(b"admin> ")
                    continue
                if cmd in {"quit", "exit"}:
                    self.request.sendall(b"Bye\r\n")
                    break
                if cmd.startswith("mode "):
                    choice = cmd[5:].strip()
                    if choice in {"vulnerable", "fixed"}:
                        variant = choice
                        self.request.sendall(f"Mode: {variant}\r\nadmin> ".encode())
                    else:
                        self.request.sendall(b"Usage: mode vulnerable|fixed\r\nadmin> ")
                    continue
                if cmd == "status":
                    res = resolver.run("python/error-disclosure", "error", variant=variant)
                    body = res[2] if res else "unavailable"
                    self.request.sendall((body + "\r\nadmin> ").encode())
                    continue
                if cmd.startswith("ping "):
                    arg = cmd[5:]
                    res = resolver.run("python/command-injection", arg, variant=variant)
                    body = res[2] if res else "unavailable"
                    self.request.sendall((body + "\r\nadmin> ").encode())
                    continue
                if cmd.startswith("help "):
                    arg = cmd[5:].strip()
                    res = resolver.run("python/jenkins-cli-atfile", {"args": [arg]}, variant=variant)
                    body = res[2] if res else "unavailable"
                    self.request.sendall((body + "\r\nadmin> ").encode())
                    continue
                self.request.sendall(b"Unknown command.\r\nadmin> ")

    return Handler


# --------------------------------------------------------------------------- SMTP (2525)
def make_smtp_handler(resolver):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            variant = resolver.default_variant
            recipients = []
            sender = ""

            def send(msg):
                self.request.sendall((msg + "\r\n").encode())

            send("220 badass-smtp.local ESMTP BADASS")
            while True:
                line = _readline(self.request)
                if line is None:
                    break
                verb, _, arg = line.partition(" ")
                cmd = verb.upper()
                arg = arg.strip()
                if cmd in {"HELO", "EHLO"}:
                    res = resolver.run("python/log-injection", arg, variant=variant)
                    out = res[2] if res else arg
                    if cmd == "EHLO":
                        send(f"250-badass-smtp.local greets {out.splitlines()[0]}")
                        send("250 VRFY")
                    else:
                        send(f"250 badass-smtp.local greets {out.splitlines()[0]}")
                elif cmd == "VRFY":
                    if variant == "vulnerable":
                        if arg.lower() in {"alice", "alice@example.test"}:
                            send("250 2.1.5 <alice@example.test>")
                        elif arg.lower() in {"bob", "bob@example.test"}:
                            send("250 2.1.5 <bob@example.test>")
                        else:
                            send("550 5.1.1 User unknown")
                    else:
                        send("252 2.1.5 Cannot VRFY user, but will accept message")
                elif cmd == "MAIL":
                    sender = arg
                    res = resolver.run("python/header-injection", sender, variant=variant)
                    if res and res[2] == "DENIED":
                        send("550 5.5.2 Invalid sender header")
                    else:
                        send("250 2.1.0 Ok")
                elif cmd == "RCPT":
                    addr = arg.replace("TO:", "").replace("to:", "").strip().strip("<>")
                    recipients.append(addr)
                    send("250 2.1.5 Ok")
                elif cmd == "DATA":
                    send("354 End data with <CR><LF>.<CR><LF>")
                    lines = []
                    while True:
                        msg_line = _readline(self.request)
                        if msg_line is None or msg_line == ".":
                            break
                        lines.append(msg_line)
                    header_check = resolver.run("python/header-injection", "\n".join(lines[:4]), variant=variant)
                    if variant == "fixed" and header_check and header_check[2] == "DENIED":
                        send("550 5.7.1 Message rejected")
                        continue
                    if recipients:
                        reset = resolver.run("python/gitlab-reset-recipients", {"email": recipients}, variant=variant)
                        if reset and reset[0] >= 400:
                            send(f"550 5.7.1 Rejected recipients: {reset[2]}")
                            recipients.clear()
                            continue
                    recipients.clear()
                    send("250 2.0.0 Ok: queued")
                elif cmd == "RSET":
                    recipients.clear()
                    sender = ""
                    send("250 2.0.0 Ok")
                elif cmd == "NOOP":
                    send("250 2.0.0 Ok")
                elif cmd == "QUIT":
                    send("221 2.0.0 Bye")
                    break
                else:
                    send("502 5.5.1 Command not implemented")

    return Handler


# --------------------------------------------------------------------------- LDAPv3 (3389)
def _ber_len(n):
    if n < 0x80:
        return bytes([n])
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(raw)]) + raw


def _ber_tlv(tag, payload):
    return bytes([tag]) + _ber_len(len(payload)) + payload


def _ber_read(data, pos=0):
    if pos >= len(data):
        raise ValueError("truncated BER")
    tag = data[pos]
    pos += 1
    first = data[pos]
    pos += 1
    if first & 0x80 == 0:
        length = first
    else:
        nbytes = first & 0x7F
        length = int.from_bytes(data[pos:pos + nbytes], "big")
        pos += nbytes
    end = pos + length
    if end > len(data):
        raise ValueError("truncated BER payload")
    return tag, data[pos:end], end


def _ldap_filter_str(data):
    tag, payload, _ = _ber_read(data, 0)
    if tag == 0xA3:  # equalityMatch: attr, val
        _, attr, p2 = _ber_read(payload, 0)
        _, val, _ = _ber_read(payload, p2)
        return attr.decode("utf-8", "replace"), val.decode("utf-8", "replace"), False
    if tag == 0x87:  # present
        return payload.decode("utf-8", "replace"), "*", True
    if tag in (0xA0, 0xA1):  # and / or
        pos, parts = 0, []
        while pos < len(payload):
            _, sub, pos_next = _ber_read(payload, pos)
            parts.append(_ldap_filter_str(payload[pos:pos_next]))
            pos = pos_next
        for attr, val, wild in parts:
            if wild or val == "*":
                return attr, "*", True
        return parts[0] if parts else ("uid", "", False)
    if tag == 0xA4:  # substrings: attr + SEQUENCE OF {0x80 initial, 0x81 any, 0x82 final}
        _, attr, p2 = _ber_read(payload, 0)
        _, seq, _ = _ber_read(payload, p2)
        p3 = 0
        parts = []
        while p3 < len(seq):
            stag, sval, p3 = _ber_read(seq, p3)
            parts.append((stag, sval.decode("utf-8", "replace")))
        initial = next((v for t, v in parts if t == 0x80), None)
        if initial and initial != "*":
            return attr.decode("utf-8", "replace"), initial, False
        return attr.decode("utf-8", "replace"), "*", True
    return "uid", "", False


def _recv_exact(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)


def _ldap_msg(msg_id, op_tag, body):
    mid = _ber_tlv(0x02, msg_id.to_bytes(max(1, (msg_id.bit_length() + 8) // 8), "big", signed=True))
    return _ber_tlv(0x30, mid + _ber_tlv(op_tag, body))


def _ldap_result(code=0, matched=b"", diag=b""):
    return _ber_tlv(0x0A, bytes([code])) + _ber_tlv(0x04, matched) + _ber_tlv(0x04, diag)


def make_ldap_handler(resolver):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            while True:
                head = _recv_exact(self.request, 2)
                if head is None:
                    break
                if head[1] & 0x80 == 0:
                    length = head[1]
                else:
                    nbytes = head[1] & 0x7F
                    if nbytes == 0 or nbytes > 4:
                        break
                    len_bytes = _recv_exact(self.request, nbytes)
                    if len_bytes is None:
                        break
                    length = int.from_bytes(len_bytes, "big")
                if length > 65536:
                    break
                payload = _recv_exact(self.request, length)
                if payload is None:
                    break
                try:
                    _, mid_bytes, pos = _ber_read(payload, 0)
                    msg_id = int.from_bytes(mid_bytes, "big", signed=True)
                    op_tag, op_body, _ = _ber_read(payload, pos)
                except (ValueError, IndexError):
                    break
                if op_tag == 0x60:  # BindRequest
                    self.request.sendall(_ldap_msg(msg_id, 0x61, _ldap_result(0)))
                elif op_tag == 0x42:  # UnbindRequest
                    break
                elif op_tag == 0x63:  # SearchRequest
                    p = 0
                    for _ in range(6):  # baseObject, scope, deref, sizeLimit, timeLimit, typesOnly
                        _, _, p = _ber_read(op_body, p)
                    _, _, p_end = _ber_read(op_body, p)
                    attr, val, is_wild = _ldap_filter_str(op_body[p:p_end])
                    query = "*" if is_wild else val
                    res = resolver.run("python/ldap-injection", query)
                    mail = res[2] if res and res[0] == 200 else "NOT_FOUND"
                    if mail not in {"NOT_FOUND", "DENIED"}:
                        uid = "admin" if "admin" in mail else "alice"
                        dn = f"uid={uid},ou=users,dc=badass,dc=local".encode()
                        attrs = _ber_tlv(0x30, (
                            _ber_tlv(0x30, _ber_tlv(0x04, b"uid") + _ber_tlv(0x31, _ber_tlv(0x04, uid.encode())))
                            + _ber_tlv(0x30, _ber_tlv(0x04, b"mail") + _ber_tlv(0x31, _ber_tlv(0x04, mail.encode())))
                        ))
                        self.request.sendall(_ldap_msg(msg_id, 0x64, _ber_tlv(0x04, dn) + attrs))
                    self.request.sendall(_ldap_msg(msg_id, 0x65, _ldap_result(0)))
                else:
                    self.request.sendall(_ldap_msg(msg_id, 0x78, _ldap_result(2)))

    return Handler


# --------------------------------------------------------------------------- DNS (5353/udp & tcp)
def _dns_decode_name(packet, offset):
    labels = []
    pos = offset
    while pos < len(packet):
        length = packet[pos]
        pos += 1
        if length == 0:
            break
        if length & 0xC0:
            pos += 1
            break
        labels.append(packet[pos:pos + length].decode("ascii", "replace"))
        pos += length
    return ".".join(labels).lower(), pos


def build_dns_reply(packet, resolver, rebind_state):
    if len(packet) < 12:
        return b""
    txid, flags, qdcount = struct.unpack("!HHH", packet[:6])
    if qdcount < 1:
        return b""
    qname, qend = _dns_decode_name(packet, 12)
    if qend + 4 > len(packet):
        return b""
    qtype, qclass = struct.unpack("!HH", packet[qend:qend + 4])
    question = packet[12:qend + 4]
    rd = flags & 0x0100
    resp_flags = 0x8180 | rd
    answers = []
    variant = resolver.default_variant

    if qtype in (1, 255):  # A or ANY
        ip = "127.0.0.1"
        if qname == "rebind.badass.local":
            if variant == "vulnerable":
                with rebind_state["lock"]:
                    rebind_state["count"] += 1
                    ip = "93.184.216.34" if rebind_state["count"] == 1 else "127.0.0.1"
            else:
                ip = "93.184.216.34"
        rdata = ipaddress.IPv4Address(ip).packed
        answers.append(struct.pack("!HHHIH", 0xC00C, 1, qclass, 1, len(rdata)) + rdata)
    if qtype in (16, 255) and qname in {"secret.badass.local", "version.bind"}:
        res = resolver.run("python/error-disclosure", "error" if variant == "vulnerable" else "ok")
        txt = (res[2] if res else "OK").encode("utf-8", "replace")[:200]
        rdata = bytes([len(txt)]) + txt
        answers.append(struct.pack("!HHHIH", 0xC00C, 16, qclass, 1, len(rdata)) + rdata)
    if not answers:
        resp_flags = 0x8183 | rd  # NXDOMAIN
    header = struct.pack("!HHHHHH", txid, resp_flags, 1, len(answers), 0, 0)
    return header + question + b"".join(answers)


def make_dns_udp_handler(resolver, rebind_state):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            data, sock = self.request
            reply = build_dns_reply(data, resolver, rebind_state)
            if reply:
                sock.sendto(reply, self.client_address)

    return Handler


def make_dns_tcp_handler(resolver, rebind_state):
    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(10)
            hdr = _recv_exact(self.request, 2)
            if hdr is None:
                return
            length = struct.unpack("!H", hdr)[0]
            data = _recv_exact(self.request, length)
            if data is None:
                return
            reply = build_dns_reply(data, resolver, rebind_state)
            if reply:
                self.request.sendall(struct.pack("!H", len(reply)) + reply)

    return Handler


# --------------------------------------------------------------------------- RESP / Redis-like (6379)
def _resp_read_cmd(sock):
    line = _readline(sock)
    if line is None:
        return None
    if not line.startswith("*"):
        return line.split()
    try:
        count = int(line[1:] or 0)
    except ValueError:
        return None
    if not 0 <= count <= 64:
        return None
    args = []
    for _ in range(count):
        hdr = _readline(sock)
        if hdr is None or not hdr.startswith("$"):
            return None
        try:
            size = int(hdr[1:])
        except ValueError:
            return None
        if not 0 <= size <= (1 << 20):
            return None
        data = _recv_exact(sock, size + 2)
        if data is None:
            return None
        args.append(data[:size].decode("utf-8", "replace"))
    return args


def _resp_bulk(text):
    raw = text.encode("utf-8", "replace")
    return f"${len(raw)}\r\n".encode() + raw + b"\r\n"


def make_resp_handler(resolver):
    store = {}
    store_lock = threading.Lock()

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            self.request.settimeout(30)
            variant = resolver.default_variant
            authed = variant == "vulnerable"
            while True:
                args = _resp_read_cmd(self.request)
                if args is None:
                    break
                if not args:
                    continue
                cmd = args[0].upper()
                if cmd == "QUIT":
                    self.request.sendall(b"+OK\r\n")
                    break
                if cmd == "PING":
                    self.request.sendall(b"+PONG\r\n")
                    continue
                if cmd == "AUTH":
                    pw = args[1] if len(args) > 1 else ""
                    res = resolver.run("python/hardcoded-credentials", pw, variant=variant)
                    if res and res[0] == 200 and res[2] == "ADMIN":
                        authed = True
                        self.request.sendall(b"+OK\r\n")
                    else:
                        self.request.sendall(b"-WRONGPASS invalid password\r\n")
                    continue
                if not authed:
                    self.request.sendall(b"-NOAUTH Authentication required.\r\n")
                    continue
                if cmd == "INFO":
                    res = resolver.run("python/error-disclosure", "error", variant=variant)
                    self.request.sendall(_resp_bulk(f"server:badass-resp\r\nbackend:{res[2] if res else 'ok'}\r\n"))
                elif cmd == "GET" and len(args) >= 2:
                    with store_lock:
                        val = store.get(args[1])
                    self.request.sendall(b"$-1\r\n" if val is None else _resp_bulk(val))
                elif cmd == "SET" and len(args) >= 3:
                    with store_lock:
                        store[args[1]] = args[2]
                    self.request.sendall(b"+OK\r\n")
                elif cmd == "EVAL" and len(args) >= 2:
                    if variant == "fixed":
                        self.request.sendall(b"-ERR EVAL disabled in fixed mode\r\n")
                        continue
                    res = resolver.run("python/code-injection", args[1], variant=variant)
                    self.request.sendall(_resp_bulk(res[2] if res else "DENIED"))
                else:
                    self.request.sendall(b"-ERR unknown or malformed command\r\n")

    return Handler


# --------------------------------------------------------------------------- lifecycle
def start_services(gateway, host, ports=None, variant="vulnerable", tls_dir=None, https_handler_factory=None):
    """Start all non-HTTP (and HTTPS) listeners in daemon threads."""
    cfg = dict(DEFAULT_PORTS)
    if ports:
        cfg.update(ports)
    resolver = Resolver(gateway, default_variant=variant)
    rebind_state = {"count": 0, "lock": threading.Lock()}
    ftp_data_box = [cfg["ftp_data"]]
    started = []

    def launch(name, transport, srv):
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        port = srv.server_address[1]
        started.append((name, port, transport, srv))

    if https_handler_factory and tls_dir is not None:
        cert, key = generate_tls_cert(Path(tls_dir))
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(certfile=str(cert), keyfile=str(key))
        https_srv = make_tls_http_server((host, cfg["https"]), https_handler_factory(gateway), ctx)
        launch("https", "tcp", https_srv)

    launch("ftp", "tcp", ThreadedTCPServer((host, cfg["ftp"]), make_ftp_handler(resolver, ftp_data_box)))
    launch("telnet", "tcp", ThreadedTCPServer((host, cfg["telnet"]), make_telnet_handler(resolver)))
    launch("smtp", "tcp", ThreadedTCPServer((host, cfg["smtp"]), make_smtp_handler(resolver)))
    launch("ldap", "tcp", ThreadedTCPServer((host, cfg["ldap"]), make_ldap_handler(resolver)))
    launch("dns", "udp", ThreadedUDPServer((host, cfg["dns"]), make_dns_udp_handler(resolver, rebind_state)))
    launch("dns", "tcp", ThreadedTCPServer((host, cfg["dns"]), make_dns_tcp_handler(resolver, rebind_state)))
    launch("resp", "tcp", ThreadedTCPServer((host, cfg["resp"]), make_resp_handler(resolver)))
    launch("tcp", "tcp", ThreadedTCPServer((host, cfg["tcp"]), make_tcp_handler(gateway)))
    return started
