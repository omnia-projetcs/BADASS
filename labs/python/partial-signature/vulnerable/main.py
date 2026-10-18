"""A caller-controlled tag length truncates the expected HMAC comparison."""
import hashlib
import hmac
from pathlib import Path
import re
import secrets


def sign(body, key):
    return hmac.new(key, body, hashlib.sha256).hexdigest()


def verify(body, tag, key):
    if not isinstance(tag, str) or not re.fullmatch(r"[0-9a-f]{0,64}", tag):
        return False
    expected = sign(body, key)
    # Even constant-time comparison is unsafe when the caller chooses its length.
    return hmac.compare_digest(expected[:len(tag)], tag)


def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("body"), str):
        return {"status": 400}
    mode = request.get("signature")
    if mode not in ("valid", "prefix", "empty", "wrong", "malformed"):
        return {"status": 400}
    try:
        body = request["body"].encode("utf-8")
    except UnicodeError:
        return {"status": 400}
    if len(body) > 256:
        return {"status": 400}
    # Signature selectors are trusted scenario controls, not a signing API.
    key = secrets.token_bytes(32)
    tag = sign(body, key)
    if mode == "prefix":
        tag = tag[:2]
    elif mode == "empty":
        tag = ""
    elif mode == "wrong":
        tag = ("0" if tag[0] != "0" else "1") + tag[1:]
    elif mode == "malformed":
        tag = "not-a-tag"
    if not verify(body, tag, key):
        return {"status": 401}
    Path("verified-message.txt").write_bytes(body)
    return {"status": 201, "bytes": len(body)}
