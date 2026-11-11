import json
import os
from urllib.parse import parse_qs


def evaluate(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        return "DENIED"
    if isinstance(value, str) and (len(value) > 16 or value.strip().startswith("-0")):
        return "DENIED"
    try:
        quantity = int(value)
    except ValueError:
        return "DENIED"
    if not 1 <= quantity <= 100:
        return "DENIED"
    return str(1000 - quantity * 10)


def run(query_string):
    value = parse_qs(query_string, keep_blank_values=True).get("value", [""])[0]
    result = evaluate(value)
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)


if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
