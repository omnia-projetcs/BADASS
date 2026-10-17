"""Session rotation after a principal was authenticated by the trusted caller."""
import re
import secrets


def _valid_id(session_id):
    return isinstance(session_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,128}", session_id) is not None


def login(old_id, principal, sessions):
    # Principal is supplied by the authentication fixture, never by request JSON.
    if not _valid_id(old_id) or not isinstance(principal, str) or not principal:
        return None
    for _ in range(4):
        new_id = secrets.token_urlsafe(32)
        if new_id != old_id and new_id not in sessions:
            break
    else:
        return None
    sessions.pop(old_id, None)
    sessions[new_id] = principal
    return new_id


def resolve_session(session_id, sessions):
    return sessions.get(session_id) if _valid_id(session_id) else None


def logout(session_id, sessions):
    if not _valid_id(session_id) or session_id not in sessions:
        return False
    del sessions[session_id]
    return True
