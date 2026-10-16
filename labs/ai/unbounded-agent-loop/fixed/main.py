def run(requested_steps):
    if type(requested_steps) is not int or not 0 <= requested_steps <= 5:
        return 'DENIED'
    return sum(1 for _ in range(requested_steps))
