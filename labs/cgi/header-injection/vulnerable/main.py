from urllib.parse import unquote
import os
def run(value):
    return 'Location: ' + unquote(value) + '\r\n\r\n'
if __name__ == '__main__':
    print(run(os.environ.get('QUERY_STRING', '/')), end='')
