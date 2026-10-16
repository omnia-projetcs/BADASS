import hmac, os
def run(password):
    expected = os.environ.get('BADASS_ADMIN_PASSWORD')
    if not expected:
        return 'DENIED'
    return 'ADMIN' if hmac.compare_digest(password, expected) else 'DENIED'
