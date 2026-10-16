import hashlib
def run(value):
    if not value:
        return 'DENIED'
    stored = hashlib.md5(value.encode()).hexdigest()
    return {'password_matches': stored == hashlib.md5(value.encode()).hexdigest(), 'legacy_md5': len(stored) == 32}
