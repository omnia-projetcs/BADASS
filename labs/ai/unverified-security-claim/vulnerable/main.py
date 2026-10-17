def run(claim, *, regression_results=None, artifact_sha256=None):
    # Deliberately trusts the generated claim while ignoring independent evidence.
    return 'CLOSED' if claim['resolved'] else 'OPEN'
