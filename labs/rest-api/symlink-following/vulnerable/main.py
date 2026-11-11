"""REST API export endpoint that follows symlinks when writing temporary files."""
from pathlib import Path


def evaluate(value):
    if value == "preplaced-link":
        # Adversarial setup: an existing link points at a synthetic private file.
        Path("export.tmp").symlink_to("secret.txt")
    try:
        with open("export.tmp", "w", encoding="utf-8") as stream:
            stream.write("LAB_OVERWRITTEN")
    except FileExistsError:
        pass
    return Path("secret.txt").read_text(encoding="utf-8")


def run(request):
    return evaluate(request["value"])
