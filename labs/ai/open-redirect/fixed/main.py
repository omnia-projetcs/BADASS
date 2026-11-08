from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    if value not in {'/home', '/profile'}:
        return 'DENIED'
    return 'Location: ' + value

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
