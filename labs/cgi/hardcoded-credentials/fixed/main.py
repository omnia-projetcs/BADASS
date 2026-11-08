import hmac
import json
import os
from urllib.parse import parse_qs


def _password_bytes(value):
    if not isinstance(value, str) or not value or len(value) > 1024:
        return None
    try:
        return value.encode("utf-8")
    except UnicodeEncodeError:
        return None


def evaluate(value):
    expected = _password_bytes(os.environ.get("BADASS_ADMIN_PASSWORD"))
    supplied = _password_bytes(value)
    if expected is None or supplied is None:
        return "DENIED"
    return "ADMIN" if hmac.compare_digest(supplied, expected) else "DENIED"


def run(query_string):
    result = "DENIED"
    if isinstance(query_string, str) and len(query_string) <= 16384:
        try:
            query_string.encode("utf-8")
            values = parse_qs(
                query_string, keep_blank_values=True, errors="strict", max_num_fields=16,
            ).get("value", [])
            if len(values) == 1:
                result = evaluate(values[0])
        except (ValueError, UnicodeError):
            pass
    return "Content-Type: application/json\r\n\r\n" + json.dumps(result)


if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "")), end="")
