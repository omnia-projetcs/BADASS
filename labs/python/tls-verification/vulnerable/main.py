import ssl
def run(value):
    if value == 'noop':
        return 'OK'
    context = ssl._create_unverified_context()
    return context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
