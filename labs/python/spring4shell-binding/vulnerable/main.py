"""Bind public form fields and write a synthetic access log."""
from pathlib import Path
import re


def run(request):
    fields = request.get("fields") if isinstance(request, dict) else None
    if not isinstance(fields, dict) or len(fields) > 8:
        return {"status": 400, "error": "invalid binding"}
    model = {"name": "alice", "profile": {"display_name": "Alice"},
             "class": {"module": {"classLoader": {"pipeline": {"prefix": "access"}}}}}
    try:
        for key, value in fields.items():
            if not isinstance(key, str) or len(key) > 128 or not isinstance(value, str) or len(value) > 64 or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in key + value):
                raise ValueError("invalid field")
        pass
        for key, value in fields.items():
            node = model
            parts = key.split(".")
            for part in parts[:-1]:
                node = node[part]
                if not isinstance(node, dict): raise ValueError("not an object")
            if parts[-1] not in node: raise ValueError("unknown field")
            node[parts[-1]] = value
        prefix = model["class"]["module"]["classLoader"]["pipeline"]["prefix"]
        if not re.fullmatch(r"[a-z]{1,20}", prefix): raise ValueError("invalid prefix")
        Path("logs").mkdir(exist_ok=True)
        Path("logs", prefix + ".log").write_text("user=" + model["name"] + "\n", encoding="utf-8")
        return {"status": 200, "name": model["name"], "display_name": model["profile"]["display_name"]}
    except (KeyError, TypeError, ValueError):
        return {"status": 400, "error": "invalid binding"}
