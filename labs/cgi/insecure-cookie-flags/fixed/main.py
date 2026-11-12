"""CGI session handler enforcing Secure, HttpOnly, and SameSite=Strict on session cookies."""
import re
from urllib.parse import parse_qs


def run(query_string):
    if not isinstance(query_string, str):
        return "Status: 400 Bad Request\r\n\r\nDENIED"
    params = parse_qs(query_string, keep_blank_values=True)
    mode = params.get("mode", ["cookie"])[0]
    if mode == "ping":
        return "Status: 200 OK\r\nContent-Type: text/plain\r\n\r\nPONG"
    sid = params.get("sid", [""])[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", sid):
        return "Status: 400 Bad Request\r\n\r\nDENIED"
    cookie = f"session={sid}; Path=/; Secure; HttpOnly; SameSite=Strict"
    return f"Set-Cookie: {cookie}\r\nContent-Type: text/plain\r\n\r\nOK"
