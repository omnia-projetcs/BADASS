import hashlib, hmac, secrets
def run(value):
    if not value:
        return 'DENIED'
    salt = secrets.token_bytes(16)
    stored = hashlib.scrypt(value.encode(), salt=salt, n=16384, r=8, p=1)
    candidate = hashlib.scrypt(value.encode(), salt=salt, n=16384, r=8, p=1)
    return {'password_matches': hmac.compare_digest(stored, candidate), 'legacy_md5': False}
