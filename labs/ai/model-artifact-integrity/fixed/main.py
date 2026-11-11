"""Model loader that verifies the artifact SHA-256 digest before activation."""
import hashlib
import hmac

EXPECTED = hashlib.sha256(b"approved-model").digest()


def run(artifact):
    if not isinstance(artifact, str):
        return "DENIED"
    try:
        digest = hashlib.sha256(artifact.encode("utf-8")).digest()
    except UnicodeEncodeError:
        return "DENIED"
    if not hmac.compare_digest(digest, EXPECTED):
        return "DENIED"
    return artifact
