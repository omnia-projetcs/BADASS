from pathlib import Path
import os
import hmac
import html
import subprocess

def run(value):
    if '\r' in value or '\n' in value:
        return 'DENIED'
    return 'X-User: ' + value + '\r\n\r\nBODY'
