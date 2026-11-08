import html
def run(output):
    return '<p>' + html.escape(output, quote=False) + '</p>'
