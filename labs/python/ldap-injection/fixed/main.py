"""Directory search filter builder escaping RFC 4515 special characters and enforcing identifier bounds."""
import re

DIRECTORY = [
    {"uid": "alice", "role": "user", "mail": "alice@example.test"},
    {"uid": "admin", "role": "admin", "mail": "secret-admin@example.test"},
]


def escape_ldap(value):
    mapping = {"\\": r"\5c", "*": r"\2a", "(": r"\28", ")": r"\29", "\x00": r"\00"}
    return "".join(mapping.get(ch, ch) for ch in value)


def run(username):
    if not isinstance(username, str) or not re.fullmatch(r"[a-z0-9_-]{1,32}", username):
        return "DENIED"
    safe_uid = escape_ldap(username)
    for entry in DIRECTORY:
        if entry["uid"] == safe_uid and entry["role"] == "user":
            return entry["mail"]
    return "NOT_FOUND"
