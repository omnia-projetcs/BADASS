from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    if value == 'ok':
        return 'OK'
    try:
        Path('missing-database').read_text()
    except FileNotFoundError:
        return 'Service unavailable'
    return 'OK'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
