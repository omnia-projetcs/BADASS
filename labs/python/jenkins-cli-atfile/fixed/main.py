"""Process CLI arguments without expanding @file references."""
import hmac


def expand(argument):
    raise RuntimeError("Argument file expansion is disabled")


def run(request):
    args = request.get("args") if isinstance(request, dict) else None
    if not isinstance(args, list) or not 1 <= len(args) <= 4 or any(not isinstance(a, str) or len(a) > 128 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in a) for a in args):
        return {"status": 400, "error": "invalid command"}
    try:
        expanded = args.copy()
        if not expanded: return {"status": 400, "error": "invalid command"}
        token = request.get("token")
        if not isinstance(token, str) or not hmac.compare_digest(token.encode("utf-8", errors="replace"), b"LAB_CLI_READER"):
            return {"status": 403, "argument": expanded[0]}
        return {"status": 200, "arguments": expanded}
    except (ValueError, OSError, UnicodeError):
        return {"status": 400, "error": "invalid command"}
