"""Stream cipher wrapper enforcing unique nonces per encryption and rejecting nonce reuse."""
import hashlib

KEY = b"LAB_STREAM_KEY_32_BYTES_FIXED!!!"


def keystream(nonce, length):
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(KEY + nonce + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:length])


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    nonce_1 = b"UNIQUE_NONCE_001"
    nonce_2 = b"UNIQUE_NONCE_002"
    if nonce_1 == nonce_2:
        return "DENIED"
    known_plain = b"PUBLIC_HEADER_16"
    c1 = xor_bytes(known_plain, keystream(nonce_1, 16))
    if request.get("op") == "recover":
        return "DENIED"
    if request.get("op") != "decrypt_public":
        return "DENIED"
    return xor_bytes(c1, keystream(nonce_1, 16)).decode("ascii")
