import hashlib, hmac
EXPECTED = hashlib.sha256(b'approved-model').digest()
def run(artifact):
    if not hmac.compare_digest(hashlib.sha256(artifact.encode()).digest(), EXPECTED):
        return 'DENIED'
    return artifact
