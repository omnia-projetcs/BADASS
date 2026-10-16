def run(claim):
    return 'CLOSED' if claim['resolved'] else 'OPEN'
