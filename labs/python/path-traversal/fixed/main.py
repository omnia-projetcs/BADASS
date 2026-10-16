from pathlib import Path
def run(value):
    if value != 'welcome.txt':
        return 'DENIED'
    return Path('public/welcome.txt').read_text()
