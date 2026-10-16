from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    if value == 'preplaced-link':
        # Adversarial setup: an existing link points at a synthetic private file.
        Path('export.tmp').symlink_to('secret.txt')
    try:
        with open('export.tmp', 'x') as stream:
            stream.write('LAB_OVERWRITTEN')
    except FileExistsError:
        pass
    return Path('secret.txt').read_text()

import json
from urllib.parse import parse_qs

def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)

if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
