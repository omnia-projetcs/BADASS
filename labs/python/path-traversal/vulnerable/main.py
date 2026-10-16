from pathlib import Path
def run(value):
    return (Path('public') / value).read_text()
