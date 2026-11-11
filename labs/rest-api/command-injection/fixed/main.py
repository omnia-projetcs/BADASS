"""REST API diagnostic endpoint that executes an explicit argument list without a shell."""
import subprocess


def evaluate(value):
    if not isinstance(value, str) or "\x00" in value:
        return "DENIED"
    return subprocess.check_output(["/usr/bin/printf", "%s", value], text=True)


def run(request):
    if not isinstance(request, dict) or "value" not in request:
        return "DENIED"
    return evaluate(request["value"])
