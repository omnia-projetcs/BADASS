import hmac
import os


def _password_bytes(value):
    if not isinstance(value, str) or not value or len(value) > 1024:
        return None
    try:
        return value.encode("utf-8")
    except UnicodeEncodeError:
        return None


def evaluate(value):
    expected = _password_bytes(os.environ.get("BADASS_ADMIN_PASSWORD"))
    supplied = _password_bytes(value)
    if expected is None or supplied is None:
        return "DENIED"
    return "ADMIN" if hmac.compare_digest(supplied, expected) else "DENIED"


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
