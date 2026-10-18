"""Restricted HS256 teaching verifier; account status validation inspired by EDB-51992."""
import base64
import hashlib
import hmac
import json
import os
import re


# Fixed clock and account store make this disposable fixture deterministic.
NOW = 2_000_000_000
USERS = {"alice": {"active": True, "role": "reader"},
         "admin": {"active": True, "role": "admin"},
         "bob": {"active": False, "role": "reader"}}


def decode_segment(segment):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", segment):
        raise ValueError("invalid base64url")
    raw = base64.b64decode(segment + "=" * (-len(segment) % 4), altchars=b"-_", validate=True)
    if base64.urlsafe_b64encode(raw).decode().rstrip("=") != segment:
        raise ValueError("noncanonical base64url")
    return raw


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON property")
        result[key] = value
    return result


def signing_key():
    # The deployment must supply a random key; length alone cannot prove entropy.
    value = os.environ.get("BADASS_JWT_KEY", "")
    try:
        key = value.encode("utf-8")
    except UnicodeEncodeError:
        return None
    return key if 32 <= len(key) <= 256 else None


def verify(token, key):
    if not isinstance(token, str) or len(token) > 4096:
        return None
    try:
        header_segment, claims_segment, signature_segment = token.split(".")
        header = json.loads(decode_segment(header_segment).decode("utf-8"), object_pairs_hook=unique_object)
        if header != {"alg": "HS256", "typ": "JWT"}:
            return None
        signing_input = (header_segment + "." + claims_segment).encode("ascii")
        expected = hmac.new(key, signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(expected, decode_segment(signature_segment)):
            return None
        claims = json.loads(decode_segment(claims_segment).decode("utf-8"), object_pairs_hook=unique_object)
        if (not isinstance(claims, dict) or claims.get("iss") != "badass-fixture"
                or claims.get("aud") != "badass-api"
                or not isinstance(claims.get("sub"), str)
                or type(claims.get("exp")) is not int or claims["exp"] <= NOW
                or type(claims.get("nbf")) is not int or claims["nbf"] > NOW):
            return None
        return claims["sub"]
    except (ValueError, TypeError, UnicodeError, RecursionError):
        return None


def run(request):
    key = signing_key()
    if key is None:
        return {"status": 503, "error": "signing key unavailable"}
    subject = verify(request.get("token"), key) if isinstance(request, dict) else None
    user = USERS.get(subject)
    if user is None or not user["active"]:
        return {"status": 401, "error": "denied"}
    return {"status": 200, "user": subject, "role": user["role"]}
