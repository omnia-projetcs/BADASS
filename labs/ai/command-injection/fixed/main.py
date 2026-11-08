from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    return subprocess.check_output(['/usr/bin/printf', '%s', value], text=True)

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
