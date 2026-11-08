"""Process CLI arguments before a synthetic help permission check."""
from pathlib import Path


def expand(argument):
    if not argument.startswith("@"): return [argument]
    target = (Path.cwd() / argument[1:]).resolve()
    if not target.is_relative_to(Path.cwd().resolve()) or not target.is_file() or target.stat().st_size > 4096:
        raise ValueError("invalid argument file")
    return target.read_text(encoding="utf-8").splitlines()


def run(request):
    args = request.get("args") if isinstance(request, dict) else None
    if not isinstance(args, list) or not 1 <= len(args) <= 4 or any(not isinstance(a, str) or len(a) > 128 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in a) for a in args):
        return {"status": 400, "error": "invalid command"}
    try:
        expanded = [line for argument in args for line in expand(argument)]
        if not expanded: return {"status": 400, "error": "invalid command"}
        if request.get("token") != "LAB_CLI_READER":
            return {"status": 403, "argument": expanded[0]}
        return {"status": 200, "arguments": expanded}
    except (ValueError, OSError, UnicodeError):
        return {"status": 400, "error": "invalid command"}
