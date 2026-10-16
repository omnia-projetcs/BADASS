from pathlib import Path
import os
import hmac
import html
import subprocess

def run(value):
    if value == 'preplaced-link':
        # Adversarial setup: an existing link points at a synthetic private file.
        Path('export.tmp').symlink_to('secret.txt')
    try:
        with open('export.tmp', 'x') as stream:
            stream.write('LAB_OVERWRITTEN')
    except FileExistsError:
        pass
    return Path('secret.txt').read_text()
