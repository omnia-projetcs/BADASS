from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    return '<p>' + html.escape(value, quote=False) + '</p>'

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
