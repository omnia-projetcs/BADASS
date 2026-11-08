from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    return 'Location: ' + value

import json
from urllib.parse import parse_qs

def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return result + "\r\n\r\n" if result.startswith("Location:") else "Status: 400 Bad Request\r\n\r\n"

if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
