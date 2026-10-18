"""Literal DNS separators restrict credentialed responses to approved origins."""
import json
from pathlib import Path
import re


def response(origin, private_data="LAB_PRIVATE_PROFILE"):
    if (not isinstance(origin, str) or not 1 <= len(origin) <= 128
            or any(ord(char) < 33 or ord(char) > 126 for char in origin)):
        return {"status": 400}
    # Match exactly one permitted label followed by literal DNS separators.
    if not re.fullmatch(r"https://[a-z]+\.example\.test", origin):
        return {"status": 403}
    return {"status": 200, "headers": {"Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true"}, "body": private_data}


def run(origin):
    result = response(origin)
    if result["status"] == 200:
        Path("cors-response.json").write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    return result
