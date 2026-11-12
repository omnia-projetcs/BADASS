"""CGI session handler emitting Set-Cookie without Secure, HttpOnly or SameSite attributes."""
from urllib.parse import parse_qs


def run(query_string):
    params = parse_qs(query_string, keep_blank_values=True)
    mode = params.get("mode", ["cookie"])[0]
    if mode == "ping":
        return "Status: 200 OK\r\nContent-Type: text/plain\r\n\r\nPONG"
    sid = params.get("sid", ["anon"])[0]
    return f"Set-Cookie: session={sid}; Path=/\r\nContent-Type: text/plain\r\n\r\nOK"
