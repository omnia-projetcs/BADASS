from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    fd = os.open('stored-secret', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write('PUBLIC' if value == 'public' else 'LAB_SECRET')
    os.chmod('stored-secret', 0o644)
    return format(Path('stored-secret').stat().st_mode & 0o777, '04o')

import json
from urllib.parse import parse_qs

def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)

if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
