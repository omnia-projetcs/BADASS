"""A synchronized local attacker replaces a checked filename before it is opened."""
from pathlib import Path
import threading


def write_report(target, text, checkpoint=lambda: None):
    if target.exists() or target.is_symlink():
        return {"status": 409}
    checkpoint()  # Trusted test hook schedules an attacker between check and use.
    try:
        # Exclusive creation atomically rejects a file or symlink inserted since the check.
        with target.open("x", encoding="utf-8") as stream:
            stream.write(text)
    except FileExistsError:
        return {"status": 409}
    return {"status": 201}


def run(request):
    if (not isinstance(request, dict) or type(request.get("race")) is not bool
            or not isinstance(request.get("content"), str) or len(request["content"]) > 1024):
        return {"status": 400}
    try:
        request["content"].encode("utf-8")
    except UnicodeEncodeError:
        return {"status": 400}
    target = Path("report.txt")
    Path("victim.txt").write_text("LAB_ORIGINAL", encoding="utf-8")
    if not request["race"]:
        return write_report(target, request["content"])

    checked, swapped = threading.Event(), threading.Event()
    failures = []

    def attacker():
        try:
            if not checked.wait(2):
                raise RuntimeError("writer did not reach checkpoint")
            target.symlink_to("victim.txt")
        except BaseException as error:
            failures.append(error)
        finally:
            swapped.set()

    def checkpoint():
        checked.set()
        if not swapped.wait(2):
            raise RuntimeError("attacker did not complete")
        if failures:
            raise RuntimeError("attacker failed") from failures[0]

    thread = threading.Thread(target=attacker, daemon=True)
    thread.start()
    try:
        result = write_report(target, request["content"], checkpoint)
    finally:
        checked.set()
        thread.join(3)
    if thread.is_alive() or failures:
        raise RuntimeError("race fixture did not finish correctly")
    return result
