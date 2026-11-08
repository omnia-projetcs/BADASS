def run(value):
    value = value.replace('\\', '\\\\').replace('\r', r'\r').replace('\n', r'\n')
    return 'user=' + value
