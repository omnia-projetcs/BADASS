def run(value):
    if value == 'health':
        return {'status': 200, 'audit': []}
    return {'status': 403, 'audit': []}
