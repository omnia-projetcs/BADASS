"""Serialize a rewritten request and parse it through an offline backend."""
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote


def backend(wire):
    stream = BytesIO(wire)
    requests = []
    while stream.tell() < len(wire):
        line = stream.readline().decode("ascii").removesuffix("\r\n")
        parts = line.split(" ")
        if len(parts) != 3 or parts[0] != "GET" or parts[2] != "HTTP/1.1":
            raise ValueError("invalid start line")
        for _ in range(16):
            header = stream.readline()
            if header == b"\r\n": break
            if not header.endswith(b"\r\n") or b":" not in header: raise ValueError("invalid headers")
        else: raise ValueError("too many headers")
        requests.append(parts[1])
        if len(requests) > 4: raise ValueError("too many requests")
    return requests


def run(value):
    if not isinstance(value, str) or len(value) > 512:
        return {"status": 400, "error": "invalid proxy target"}
    try:
        decoded = unquote(value, errors="strict")
        if any(ord(c) <= 32 or ord(c) == 127 for c in decoded):
            raise ValueError("invalid target character")
        wire = ("GET /backend?q=" + decoded + " HTTP/1.1\r\nHost: backend.test\r\n\r\n").encode("ascii")
        requests = backend(wire)
        Path("upstream.http").write_bytes(wire)
        return {"status": 200, "requests": requests}
    except (ValueError, UnicodeError):
        return {"status": 400, "error": "invalid proxy target"}
