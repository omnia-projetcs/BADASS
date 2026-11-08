from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    quantity = int(value)
    if not 1 <= quantity <= 100:
        return 'DENIED'
    return str(1000 - quantity * 10)

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
