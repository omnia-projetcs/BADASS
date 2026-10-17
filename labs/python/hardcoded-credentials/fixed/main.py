import hmac
import os


def _password_bytes(value):
    if not isinstance(value, str) or not value or len(value) > 1024:
        return None
    try:
        return value.encode("utf-8")
    except UnicodeEncodeError:
        return None


def run(password):
    expected = _password_bytes(os.environ.get("BADASS_ADMIN_PASSWORD"))
    supplied = _password_bytes(password)
    if expected is None or supplied is None:
        return "DENIED"
    return "ADMIN" if hmac.compare_digest(supplied, expected) else "DENIED"
