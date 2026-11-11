def run(value):
    if not isinstance(value, str) or '\r' in value or '\n' in value or '\x00' in value:
        return 'DENIED'
    return 'X-User: ' + value + '\r\n\r\nBODY'
