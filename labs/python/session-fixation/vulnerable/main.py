"""Intentional CWE-384: login upgrades the client-selected session identifier."""
import re


def _valid_id(session_id):
    return isinstance(session_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,128}", session_id) is not None


def login(old_id, principal, sessions):
    # Principal is supplied by the authentication fixture, never by request JSON.
    if not _valid_id(old_id) or not isinstance(principal, str) or not principal:
        return None
    sessions[old_id] = principal
    return old_id


def resolve_session(session_id, sessions):
    return sessions.get(session_id) if _valid_id(session_id) else None


def logout(session_id, sessions):
    if not _valid_id(session_id) or session_id not in sessions:
        return False
    del sessions[session_id]
    return True
