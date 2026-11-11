import hashlib, hmac
APPROVED = hashlib.sha256(b"RESULT = 'OK'").hexdigest()
def run(code):
    if not isinstance(code, str) or not hmac.compare_digest(hashlib.sha256(code.encode('utf-8', errors='replace')).hexdigest(), APPROVED):
        return 'DENIED'
    namespace = {}
    exec(code, namespace)
    return namespace['RESULT']
