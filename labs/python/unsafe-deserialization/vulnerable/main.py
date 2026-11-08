import base64, json, pickle
def run(value):
    if value['format'] == 'json':
        return json.loads(value['data'])
    return pickle.loads(base64.b64decode(value['data']))
