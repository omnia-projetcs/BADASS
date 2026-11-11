"""Model loader that activates an artifact without verifying its SHA-256 digest."""
import hashlib

APPROVED_DIGEST = hashlib.sha256(b"approved-model").hexdigest()


def run(artifact):
    # Vulnerable: skips comparing sha256(artifact) against APPROVED_DIGEST.
    return artifact
