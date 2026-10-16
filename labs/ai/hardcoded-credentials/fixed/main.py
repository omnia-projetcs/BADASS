from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    expected = os.environ.get('BADASS_ADMIN_PASSWORD', '')
    return 'ADMIN' if expected and hmac.compare_digest(value, expected) else 'DENIED'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
