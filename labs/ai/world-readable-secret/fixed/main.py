from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    fd = os.open('stored-secret', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write('PUBLIC' if value == 'public' else 'LAB_SECRET')
    os.chmod('stored-secret', 0o644 if value == 'public' else 0o600)
    return format(Path('stored-secret').stat().st_mode & 0o777, '04o')

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
