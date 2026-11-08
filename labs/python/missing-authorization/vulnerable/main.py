from pathlib import Path
import os
import hmac
import html
import subprocess

def run(value):
    if value == 'health':
        return 'HEALTHY'
    role = 'user'  # Trusted server-side role, not client input.
    return 'USERS_DELETED'
