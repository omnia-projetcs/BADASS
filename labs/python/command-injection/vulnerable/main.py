import subprocess
def run(value):
    return subprocess.check_output('printf %s ' + value, shell=True, text=True)
