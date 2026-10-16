def run(claim):
    # Trusted test results remain separate from model-generated claims.
    regression_passed = False
    return 'CLOSED' if claim['resolved'] and regression_passed else 'OPEN'
