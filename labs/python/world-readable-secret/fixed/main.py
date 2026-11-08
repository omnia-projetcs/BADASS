import os
from pathlib import Path
def run(value):
    if value != 'store':
        return 'IGNORED'
    fd = os.open('stored-secret', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write('LAB_SECRET')
    return oct(Path('stored-secret').stat().st_mode & 0o777)
