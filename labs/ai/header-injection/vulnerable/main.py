from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    return 'X-User: ' + value + '\r\n\r\nBODY'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
