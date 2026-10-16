import hashlib, secrets
def run(value):
    if not value:
        return 'DENIED'
    token = secrets.token_hex(32)
    return token == hashlib.md5(value.encode()).hexdigest()
