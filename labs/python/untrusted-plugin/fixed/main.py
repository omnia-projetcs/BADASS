import runpy
from pathlib import Path
def run(name):
    Path('trusted.py').write_text("RESULT = 'OK'")
    Path('untrusted.py').write_text("RESULT = 'LAB_EXECUTED'")
    if name != 'trusted.py':
        return 'DENIED'
    return runpy.run_path('trusted.py')['RESULT']
