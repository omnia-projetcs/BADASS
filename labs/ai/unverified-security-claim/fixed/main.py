import re


def run(claim, *, regression_results=None, artifact_sha256=None):
    """Evidence is supplied by the application, independently of model output."""
    if not isinstance(claim, dict) or claim.get("resolved") is not True:
        return "OPEN"
    if not isinstance(artifact_sha256, str) or re.fullmatch(r"[0-9a-f]{64}", artifact_sha256) is None:
        return "OPEN"
    if not isinstance(regression_results, dict):
        return "OPEN"
    if regression_results.get("artifact_sha256") != artifact_sha256:
        return "OPEN"
    checks = regression_results.get("checks")
    if not isinstance(checks, list) or not checks:
        return "OPEN"
    if not all(isinstance(check, dict) and check.get("status") == "pass" for check in checks):
        return "OPEN"
    return "CLOSED"
