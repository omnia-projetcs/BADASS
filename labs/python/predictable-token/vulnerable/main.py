import hashlib
def run(value):
    if not value:
        return 'DENIED'
    token = hashlib.md5(value.encode()).hexdigest()
    return token == hashlib.md5(value.encode()).hexdigest()
