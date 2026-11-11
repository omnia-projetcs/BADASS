from urllib.parse import unquote
import os


def run(value):
    if not isinstance(value, str):
        return "Status: 400 Bad Request\r\n\r\n"
    value = unquote(value)
    if (
        not value.startswith("/")
        or value.startswith("//")
        or "\\" in value
        or any(ord(ch) < 32 or ord(ch) == 127 for ch in value)
    ):
        return "Status: 400 Bad Request\r\n\r\n"
    return "Location: " + value + "\r\n\r\n"


if __name__ == "__main__":
    print(run(os.environ.get("QUERY_STRING", "/")), end="")
