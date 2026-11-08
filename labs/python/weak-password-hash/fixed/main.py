"""A real password record and verifier using the benchmark's scrypt profile.

The small local fixture profile is explicit; calibrate production work factors
against the deployment's password policy and resource budget.
"""
import hashlib
import hmac
import secrets

SALT_BYTES = 16
SCRYPT_N = 16384
SCRYPT_R = 8
SCRYPT_P = 1
KEY_BYTES = 32
MAXMEM = 64 * 1024 * 1024


def _password_bytes(password):
    if not isinstance(password, str) or not password or len(password) > 1024:
        return None
    try:
        return password.encode("utf-8")
    except UnicodeEncodeError:
        return None


def hash_password(password):
    encoded = _password_bytes(password)
    if encoded is None:
        return None
    salt = secrets.token_bytes(SALT_BYTES)
    derived = hashlib.scrypt(
        encoded, salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
        dklen=KEY_BYTES, maxmem=MAXMEM,
    )
    return {
        "algorithm": "scrypt", "salt": salt.hex(), "digest": derived.hex(),
        "n": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P,
    }


def verify_password(password, record):
    encoded = _password_bytes(password)
    if encoded is None or not isinstance(record, dict):
        return False
    # This fixture supports one server-selected profile, never arbitrary work
    # factors supplied by a client or by an unvalidated stored record.
    if record.get("algorithm") != "scrypt" or any(
        type(record.get(key)) is not int or record[key] != expected
        for key, expected in (("n", SCRYPT_N), ("r", SCRYPT_R), ("p", SCRYPT_P))
    ):
        return False
    salt_hex, digest_hex = record.get("salt"), record.get("digest")
    if not isinstance(salt_hex, str) or not isinstance(digest_hex, str):
        return False
    if len(salt_hex) != SALT_BYTES * 2 or len(digest_hex) != KEY_BYTES * 2:
        return False
    try:
        salt, stored = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
    except ValueError:
        return False
    if len(salt) != SALT_BYTES or len(stored) != KEY_BYTES:
        return False
    candidate = hashlib.scrypt(
        encoded, salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
        dklen=KEY_BYTES, maxmem=MAXMEM,
    )
    return hmac.compare_digest(stored, candidate)
