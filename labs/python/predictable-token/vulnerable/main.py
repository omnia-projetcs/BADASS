"""Intentional CWE-330: the account name determines the usable reset token."""
import hashlib
import hmac


def _valid_account(account):
    if not isinstance(account, str) or not account or len(account) > 256:
        return False
    try:
        account.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def issue_reset_token(account, tokens):
    if not _valid_account(account):
        return None
    token = hashlib.md5(account.encode("utf-8")).hexdigest()
    tokens[account] = token
    return token


def validate_reset_token(account, supplied, tokens):
    if not _valid_account(account) or not isinstance(supplied, str) or not supplied.isascii():
        return False
    expected = tokens.get(account)
    return isinstance(expected, str) and hmac.compare_digest(supplied, expected)


def consume_reset_token(account, supplied, tokens):
    if not validate_reset_token(account, supplied, tokens):
        return False
    del tokens[account]
    return True
