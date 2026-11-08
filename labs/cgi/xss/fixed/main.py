from urllib.parse import parse_qs
import html
import os
def run(query):
    value = parse_qs(query).get('name', [''])[0]
    return 'Content-Type: text/html\r\n\r\n<p>' + html.escape(value, quote=False) + '</p>'
if __name__ == '__main__':
    print(run(os.environ.get('QUERY_STRING', '')), end='')
