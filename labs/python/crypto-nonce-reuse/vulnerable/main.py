"""Stream cipher wrapper reusing a static all-zero nonce across encrypted records."""
import hashlib

KEY = b"LAB_STREAM_KEY_32_BYTES_FIXED!!!"
STATIC_NONCE = b"\x00" * 16


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
    known_plain = b"PUBLIC_HEADER_16"
    secret_plain = b"LAB_SECRET_TOKEN"
    c1 = xor_bytes(known_plain, keystream(STATIC_NONCE, 16))
    c2 = xor_bytes(secret_plain, keystream(STATIC_NONCE, 16))
    if request.get("op") == "recover":
        # Two ciphertexts under the same nonce leak secret_plain = c1 ^ c2 ^ known_plain.
        recovered = xor_bytes(xor_bytes(c1, c2), known_plain).decode("ascii")
        return recovered
    return xor_bytes(c1, keystream(STATIC_NONCE, 16)).decode("ascii")
