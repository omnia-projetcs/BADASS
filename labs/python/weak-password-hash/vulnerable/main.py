"""Intentional CWE-916: functional password storage with fast, unsalted MD5."""
import hashlib
import hmac


def _password_bytes(password):
    if not isinstance(password, str) or not password or len(password) > 1024:
        return None
    try:
        return password.encode("utf-8")
    except UnicodeEncodeError:
        return None


def hash_password(password):
    encoded = _password_bytes(password)
    if encoded is None:
        return None
    return {"algorithm": "md5", "salt": "", "digest": hashlib.md5(encoded).hexdigest()}


def verify_password(password, record):
    encoded = _password_bytes(password)
    if encoded is None or not isinstance(record, dict) or record.get("algorithm") != "md5":
        return False
    stored = record.get("digest")
    if not isinstance(stored, str) or not stored.isascii():
        return False
    return hmac.compare_digest(stored, hashlib.md5(encoded).hexdigest())
