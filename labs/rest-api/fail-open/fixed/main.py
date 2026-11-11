"""REST API authorization guard that fails closed on upstream connection errors."""
import hmac


def evaluate(value):
    if not isinstance(value, str) or not value.isascii():
        return "DENIED"
    try:
        if value == "backend-down":
            raise ConnectionError("Authorization unavailable")
        return "ALLOWED" if hmac.compare_digest(value, "authorized") else "DENIED"
    except ConnectionError:
        return "DENIED"


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
