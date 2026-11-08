import subprocess
def run(value):
    return subprocess.check_output(['/usr/bin/printf', '%s', value], text=True)
