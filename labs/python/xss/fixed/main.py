import html
def run(value):
    return '<p>' + html.escape(value, quote=False) + '</p>'
