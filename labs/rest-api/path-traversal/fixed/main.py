from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    if value != 'welcome.txt':
        return 'DENIED'
    return (Path('public') / value).read_text()

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
