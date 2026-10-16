import re
def run(value):
    if len(value) > 64 or not re.fullmatch(r'[0-9]{1,8}\+[0-9]{1,8}', value):
        return 'DENIED'
    a, b = value.split('+')
    return int(a) + int(b)
