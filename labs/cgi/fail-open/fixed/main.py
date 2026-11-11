import hmac
import json
import os
from urllib.parse import parse_qs


def evaluate(value):
    if not isinstance(value, str) or not value.isascii():
        return "DENIED"
    try:
        if value == "backend-down":
            raise ConnectionError("Authorization unavailable")
        return "ALLOWED" if hmac.compare_digest(value, "authorized") else "DENIED"
    except ConnectionError:
        return "DENIED"


def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)


if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
