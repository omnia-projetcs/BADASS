def run(value):
    account = {'name': 'Alice', 'role': 'user'}
    if isinstance(value, dict) and isinstance(value.get('name'), str):
        account['name'] = value['name']
    return account
