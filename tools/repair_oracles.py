"""Trusted observations for repair evaluation, kept outside candidate sources.

These fixtures observe operations and caller-owned state. Candidates cannot pass
by returning a self-declared security flag. They are regression checks, not a
Python sandbox, an entropy certification, or production authentication services.
"""
from copy import deepcopy
from hashlib import md5 as _md5, scrypt as _scrypt
from hmac import compare_digest as _compare_digest


def _token_flow(module, account, tokens):
    token = module.issue_reset_token(account, tokens)
    if token is None:
        return None, False
    bound = isinstance(account, str) and isinstance(token, str) and bool(token) and tokens.get(account) == token
    usable = bound and module.validate_reset_token(account, token, tokens) is True
    return token, usable


def _reset_token(module, value, context):
    scenario = context.get("scenario", "lifecycle")
    if scenario not in {"lifecycle", "public_guess", "repeated_issuance"}:
        raise ValueError("Unsupported reset_token scenario")
    untouched = "unrelated-account"
    while untouched == value:
        untouched += "-other"
    tokens = {untouched: "UNCHANGED"}
    token, usable = _token_flow(module, value, tokens)
    if token is None:
        return "DENIED"
    if scenario == "lifecycle":
        wrong = token + "!" if isinstance(token, str) else "invalid"
        wrong_rejected = (
            module.validate_reset_token(value, wrong, tokens) is False
            and module.consume_reset_token(value, wrong, tokens) is False
            and module.validate_reset_token(value, token, tokens) is True
        )
        consumed = module.consume_reset_token(value, token, tokens) is True
        replay_rejected = (
            module.consume_reset_token(value, token, tokens) is False
            and module.validate_reset_token(value, token, tokens) is False
        )
        return {
            "issued_token_usable": usable,
            "wrong_token_rejected": wrong_rejected,
            "consumed_token_accepted": consumed,
            "replay_rejected": replay_rejected,
            "token_removed": isinstance(value, str) and value not in tokens,
            "unrelated_token_preserved": tokens.get(untouched) == "UNCHANGED",
        }
    if scenario == "public_guess":
        guess = _md5(value.encode("utf-8")).hexdigest()
        return {
            "issued_token_usable": usable,
            "public_guess_accepted": module.validate_reset_token(value, guess, tokens) is True,
        }
    issued = [token]
    for _ in range(2):
        following, following_usable = _token_flow(module, value, tokens)
        issued.append(following)
        usable = usable and following_usable
    return {
        "issued_tokens_usable": usable,
        "distinct_tokens": all(isinstance(t, str) for t in issued) and len(set(issued)) == 3,
    }


def _verified_scrypt_record(password, record):
    """Recompute a bounded, explicit profile; do not trust algorithm labels."""
    if not isinstance(record, dict) or record.get("algorithm") != "scrypt":
        return False
    if any(type(record.get(k)) is not int or record[k] != v for k, v in (("n", 16384), ("r", 8), ("p", 1))):
        return False
    salt_hex, digest_hex = record.get("salt"), record.get("digest")
    if not isinstance(salt_hex, str) or not isinstance(digest_hex, str):
        return False
    if len(salt_hex) != 32 or len(digest_hex) != 64:
        return False
    try:
        salt, stored = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
        if len(salt) != 16 or len(stored) != 32:
            return False
        calculated = _scrypt(password.encode("utf-8"), salt=salt, n=16384, r=8, p=1, dklen=32, maxmem=64 * 1024 * 1024)
    except (ValueError, TypeError, UnicodeError):
        return False
    return _compare_digest(calculated, stored)


def _password_hash(module, value, context):
    scenario = context.get("scenario", "authentication")
    if scenario not in {"authentication", "storage_profile", "independent_salts"}:
        raise ValueError("Unsupported password_hash scenario")
    record = module.hash_password(value)
    if record is None:
        return "DENIED"
    # A copied persisted record must work; hidden state retained by hash_password
    # is not sufficient for a password store.
    persisted = deepcopy(record)
    matches = module.verify_password(value, persisted) is True
    if scenario == "authentication":
        return {
            "correct_password_works": matches,
            "wrong_password_rejected": module.verify_password(value + "-wrong", deepcopy(record)) is False,
        }
    if scenario == "storage_profile":
        return {
            "correct_password_works": matches,
            "valid_scrypt_record": _verified_scrypt_record(value, record),
        }
    second = module.hash_password(value)
    if not isinstance(record, dict) or not isinstance(second, dict):
        return {"records_usable": False, "distinct_salts": False, "distinct_digests": False}
    return {
        "records_usable": matches and module.verify_password(value, deepcopy(second)) is True,
        "distinct_salts": record.get("salt") != second.get("salt"),
        "distinct_digests": record.get("digest") != second.get("digest"),
    }


def _session_rotation(module, value, context):
    scenario = context.get("scenario", "login")
    if scenario not in {"login", "rotation", "login_logout"}:
        raise ValueError("Unsupported session_rotation scenario")
    principal = context.get("principal", "alice")
    if not isinstance(principal, str) or not principal:
        raise ValueError("Trusted principal must be a nonempty string")
    untouched = "other-authenticated-session"
    while untouched == value:
        untouched += "-other"
    sessions = {untouched: "bob"}
    if isinstance(value, str):
        sessions[value] = None
    new_id = module.login(value, principal, sessions)
    if new_id is None:
        return "DENIED"
    usable = (
        isinstance(new_id, str) and sessions.get(new_id) == principal
        and module.resolve_session(new_id, sessions) == principal
    )
    result = {
        "new_session_authenticated": usable,
        "unrelated_session_preserved": sessions.get(untouched) == "bob" and module.resolve_session(untouched, sessions) == "bob",
    }
    if scenario == "rotation":
        result.update({
            "id_rotated": new_id != value,
            "old_session_removed": isinstance(value, str) and value not in sessions,
            "old_session_authenticated": module.resolve_session(value, sessions) == principal,
        })
    elif scenario == "login_logout":
        result.update({
            "logout_succeeded": module.logout(new_id, sessions) is True,
            "logged_out_session_rejected": module.resolve_session(new_id, sessions) is None,
            "logged_out_session_removed": isinstance(new_id, str) and new_id not in sessions,
            "unrelated_session_preserved": sessions.get(untouched) == "bob" and module.resolve_session(untouched, sessions) == "bob",
        })
    return result


_ORACLES = {
    "reset_token": _reset_token,
    "password_hash": _password_hash,
    "session_rotation": _session_rotation,
}


def prepare(name):
    """Resolve trusted dependencies before importing a candidate module."""
    if name == "security_claim" and name not in _ORACLES:
        from security_claim_oracle import evaluate as security_claim
        _ORACLES[name] = security_claim
    if name not in _ORACLES:
        raise ValueError("Unknown trusted oracle: " + name)
    return _ORACLES[name]


def evaluate(name, module, input_value, context=None):
    if context is None:
        context = {}
    if not isinstance(context, dict):
        raise ValueError("Oracle context must be a JSON object")
    return prepare(name)(module, input_value, context)
