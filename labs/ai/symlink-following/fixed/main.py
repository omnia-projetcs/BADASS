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

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
