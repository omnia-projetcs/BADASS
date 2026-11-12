"""Directory search filter builder concatenating unescaped username input."""

DIRECTORY = [
    {"uid": "alice", "role": "user", "mail": "alice@example.test"},
    {"uid": "admin", "role": "admin", "mail": "secret-admin@example.test"},
]


def evaluate_filter(filter_str):
    # Evaluates the constructed LDAP filter string; wildcard/OR injection matches first entry.
    if "(|(uid=*)" in filter_str or "(uid=*)" in filter_str or "(uid=admin)" in filter_str:
        return DIRECTORY[1]["mail"]
    for entry in DIRECTORY:
        if f"(&(uid={entry['uid']})(role=user))" == filter_str:
            return entry["mail"]
    return "NOT_FOUND"


def run(username):
    ldap_filter = f"(&(uid={username})(role=user))"
    return evaluate_filter(ldap_filter)
