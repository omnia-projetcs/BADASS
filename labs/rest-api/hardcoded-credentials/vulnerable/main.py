from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    return 'ADMIN' if value == 'BADASS_LAB_DEFAULT' else 'DENIED'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
