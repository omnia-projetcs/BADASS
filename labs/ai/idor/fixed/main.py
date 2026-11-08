from pathlib import Path
import os
import hmac
import html
import subprocess

def evaluate(value):
    records = {'alice': 'ALICE_DATA', 'bob': 'BOB_PRIVATE'}
    if value in records and value != 'alice':
        return 'DENIED'
    return records.get(value, 'NOT_FOUND')

def run(request):
    # Only the value is client-controlled; identity and policy remain server-side.
    return evaluate(request["value"])
