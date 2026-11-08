from pathlib import Path
import os
import hmac
import html
import subprocess

def run(value):
    return 'X-User: ' + value + '\r\n\r\nBODY'
