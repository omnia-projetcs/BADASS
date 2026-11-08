def run(value):
    if type(value) is not int or not 0 <= value <= 100:
        return 'DENIED'
    return len([0] * value)
