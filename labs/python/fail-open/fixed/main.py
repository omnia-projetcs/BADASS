def run(value):
    try:
        if value == 'backend-down':
            raise ConnectionError('authorization service unavailable')
        return value == 'authorized'
    except ConnectionError:
        return False
