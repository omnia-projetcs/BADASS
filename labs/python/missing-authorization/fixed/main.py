from pathlib import Path
import os
import hmac
import html
import subprocess

def run(value):
    if value == 'health':
        return 'HEALTHY'
    role = 'user'  # Trusted server-side role, not client input.
    if role != 'admin':
        return 'DENIED'
    return 'USERS_DELETED'
