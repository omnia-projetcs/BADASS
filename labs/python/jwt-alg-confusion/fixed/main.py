"""JWT verifier pinning HS256 and verifying signatures with the private HMAC secret in constant time."""
import base64
import hashlib
import hmac
import json

HMAC_SECRET = "LAB_PRIVATE_HMAC_SECRET"


def b64u_decode(segment):
    padding = "=" * ((4 - len(segment) % 4) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def run(token):
    if not isinstance(token, str) or token.count(".") != 2:
        return "DENIED"
    header_b64, payload_b64, sig_b64 = token.split(".")
    if not header_b64 or not payload_b64 or not sig_b64:
        return "DENIED"
    try:
        header = json.loads(b64u_decode(header_b64))
        payload = json.loads(b64u_decode(payload_b64))
    except Exception:
        return "DENIED"
    if not isinstance(header, dict) or not isinstance(payload, dict):
        return "DENIED"
    if header.get("alg") != "HS256" or header.get("kid") == "public":
        return "DENIED"
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected = base64.urlsafe_b64encode(
        hmac.new(HMAC_SECRET.encode("ascii"), signing_input, hashlib.sha256).digest()
    ).rstrip(b"=").decode("ascii")
    if not hmac.compare_digest(sig_b64, expected):
        return "DENIED"
    sub = payload.get("sub")
    return sub if isinstance(sub, str) else "DENIED"
