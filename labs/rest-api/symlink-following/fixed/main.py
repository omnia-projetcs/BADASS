"""REST API export endpoint that uses exclusive creation to refuse symlinks."""
from pathlib import Path


def evaluate(value):
    if not isinstance(value, str):
        return "DENIED"
    if value == "preplaced-link":
        # Adversarial setup: an existing link points at a synthetic private file.
        Path("export.tmp").symlink_to("secret.txt")
    try:
        with open("export.tmp", "x", encoding="utf-8") as stream:
            stream.write("LAB_OVERWRITTEN")
    except FileExistsError:
        pass
    return Path("secret.txt").read_text(encoding="utf-8")


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    return evaluate(request.get("value"))
