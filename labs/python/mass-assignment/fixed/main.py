def run(value):
    account = {'name': 'Alice', 'role': 'user'}
    if 'name' in value:
        account['name'] = value['name']
    return account
