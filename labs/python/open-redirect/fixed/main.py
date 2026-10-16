def run(value):
    if value not in {'/home', '/profile'}:
        return 'DENIED'
    return 'Location: ' + value
