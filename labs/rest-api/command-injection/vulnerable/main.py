"""REST API diagnostic endpoint that invokes a shell with request input."""
import subprocess


def evaluate(value):
    return subprocess.check_output("printf %s " + value, text=True, shell=True)


def run(request):
    return evaluate(request["value"])
