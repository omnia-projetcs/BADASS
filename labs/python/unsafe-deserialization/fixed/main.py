import json
def run(value):
    if value['format'] != 'json':
        return 'DENIED'
    result = json.loads(value['data'])
    return result if isinstance(result, str) else 'DENIED'
