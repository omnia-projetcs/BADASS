import json
def run(value):
    if not isinstance(value, dict) or value.get('format') != 'json' or not isinstance(value.get('data'), str):
        return 'DENIED'
    try:
        result = json.loads(value['data'])
    except (ValueError, TypeError):
        return 'DENIED'
    return result if isinstance(result, str) else 'DENIED'
