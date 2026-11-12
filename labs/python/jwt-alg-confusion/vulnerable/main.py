"""JWT verifier trusting caller-selected header algorithms including 'none' and public-key HMAC."""
import base64
import hashlib
import hmac
import json

PUBLIC_KEY_BANNER = "LAB_PUBLIC_VERIFICATION_KEY"
HMAC_SECRET = "LAB_PRIVATE_HMAC_SECRET"


def b64u_decode(segment):
    padding = "=" * ((4 - len(segment) % 4) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def run(token):
    header_b64, payload_b64, sig_b64 = token.split(".")
    header = json.loads(b64u_decode(header_b64))
    payload = json.loads(b64u_decode(payload_b64))
    alg = header.get("alg")
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    if alg == "none":
        return payload["sub"]
    key = PUBLIC_KEY_BANNER if header.get("kid") == "public" else HMAC_SECRET
    expected = base64.urlsafe_b64encode(hmac.new(key.encode(), signing_input, hashlib.sha256).digest()).rstrip(b"=").decode()
    if sig_b64 == expected:
        return payload["sub"]
    return "DENIED"
