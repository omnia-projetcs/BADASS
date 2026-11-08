import ssl
def run(value):
    if value == 'noop':
        return 'OK'
    context = ssl.create_default_context()
    return context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
