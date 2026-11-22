"""Drain all remaining FastCGI request-body bytes before reusing the connection."""
from io import BytesIO
from pathlib import Path


def run(value):
    if not isinstance(value, dict):
        return {"status": 400, "error": "invalid fpm stream"}
    wire = value.get("wire")
    read_limit = value.get("read_limit")
    if not isinstance(wire, str) or len(wire) > 2048:
        return {"status": 400, "error": "invalid fpm stream"}
    if type(read_limit) is not int or read_limit < 0:
        return {"status": 400, "error": "invalid fpm stream"}

    try:
        raw = wire.encode("ascii", errors="strict")
    except UnicodeError:
        return {"status": 400, "error": "invalid fpm stream"}

    stream = BytesIO(raw)
    executed = []
    for _ in range(8):
        if stream.tell() >= len(raw):
            break
        script_line = stream.readline().decode("ascii")
        length_line = stream.readline().decode("ascii")
        blank = stream.readline().decode("ascii")
        if not script_line.startswith("SCRIPT=") or not length_line.startswith("LENGTH=") or blank != "\n":
            return {"status": 400, "error": "malformed fastcgi frame"}
        script = script_line[len("SCRIPT="):].strip()
        try:
            content_length = int(length_line[len("LENGTH="):].strip())
        except ValueError:
            return {"status": 400, "error": "malformed fastcgi frame"}
        if not script or content_length < 0:
            return {"status": 400, "error": "malformed fastcgi frame"}

        to_read = min(content_length, read_limit)
        body_prefix = stream.read(to_read)
        if len(body_prefix) < to_read:
            return {"status": 400, "error": "truncated fastcgi body"}

        # Drain any unread request-body bytes before parsing the next request on this connection.
        remaining = content_length - to_read
        if remaining > 0:
            drained = stream.read(remaining)
            if len(drained) < remaining:
                return {"status": 400, "error": "truncated fastcgi body"}
        executed.append(script)

    Path("fpm-executed.log").write_text("\n".join(executed) + ("\n" if executed else ""), encoding="utf-8")
    return {"status": 200, "executed": executed}
