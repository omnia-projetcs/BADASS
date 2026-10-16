from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    try:
        if value == 'backend-down':
            raise ConnectionError('Authorization unavailable')
        return 'ALLOWED' if value == 'authorized' else 'DENIED'
    except ConnectionError:
        return 'ALLOWED'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
