import json
import os
from pathlib import Path
from urllib.parse import parse_qs


def evaluate(value):
    mode = 0o644 if value == "public" else 0o600
    fd = os.open("stored-secret", os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        os.fchmod(stream.fileno(), mode)
        stream.write("PUBLIC" if value == "public" else "LAB_SECRET")
    return format(Path("stored-secret").stat().st_mode & 0o777, "04o")


def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)


if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
