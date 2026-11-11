"""Build a login redirect without evaluating request-path expressions."""
from urllib.parse import quote, unquote

SECRET = "LAB_CONFLUENCE_PRIVATE"


def evaluate(expression, headers):
    raise RuntimeError("Expression evaluation is disabled")


def run(value):
    if not isinstance(value, str) or not value.startswith("/") or len(value) > 1024:
        return {"status": 400, "error": "invalid path"}
    try:
        path = unquote(value, errors="strict")
        if any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in path):
            raise ValueError("invalid character")
        headers = {"Location": "/login?next=" + quote(path, safe="")}
        # The request path is never passed to evaluate().
        return {"status": 302, "headers": headers}
    except (ValueError, SyntaxError, UnicodeError, RecursionError):
        return {"status": 400, "error": "invalid path"}
