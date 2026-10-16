from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    expected = os.environ.get('BADASS_ADMIN_PASSWORD', '')
    return 'ADMIN' if expected and hmac.compare_digest(value, expected) else 'DENIED'

import json
from urllib.parse import parse_qs

def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)

if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
