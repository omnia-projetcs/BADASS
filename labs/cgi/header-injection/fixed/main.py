from urllib.parse import unquote
import os
def run(value):
    value = unquote(value)
    if '\r' in value or '\n' in value:
        return 'Status: 400 Bad Request\r\n\r\n'
    return 'Location: ' + value + '\r\n\r\n'
if __name__ == '__main__':
    print(run(os.environ.get('QUERY_STRING', '/')), end='')
