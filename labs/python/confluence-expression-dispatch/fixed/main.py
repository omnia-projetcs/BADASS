"""Build a login redirect with a bounded pre-auth expression interpreter."""
import ast
import re
from urllib.parse import quote, unquote

SECRET = "LAB_CONFLUENCE_PRIVATE"


def evaluate(expression, headers):
    tree = ast.parse(expression.strip(), mode="eval")
    call = tree.body
    if len(list(ast.walk(tree))) > 16 or not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name) or call.func.id != "setHeader" or call.keywords or len(call.args) != 2:
        raise ValueError("unsupported expression")
    values = []
    for node in call.args:
        if isinstance(node, ast.Constant) and isinstance(node.value, str): values.append(node.value)
        elif isinstance(node, ast.Name) and node.id == "secret": values.append(SECRET)
        else: raise ValueError("unsupported argument")
    key, value = values
    if not re.fullmatch(r"X-[A-Za-z0-9-]{1,32}", key) or len(value) > 128 or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError("invalid header")
    headers[key] = value


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
