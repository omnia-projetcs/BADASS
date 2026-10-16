def run(quantity):
    if type(quantity) is not int or not 1 <= quantity <= 100:
        return 'DENIED'
    return 1000 - quantity * 10
