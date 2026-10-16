from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    record = 'user=' + value
    Path('audit.log').write_text(record)
    return Path('audit.log').read_bytes().decode()

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
