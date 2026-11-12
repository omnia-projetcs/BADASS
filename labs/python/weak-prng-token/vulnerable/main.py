"""Session token issuer using Python's non-cryptographic Mersenne Twister seeded with a timestamp."""
import random


def run(request):
    rng = random.Random(1700000000)
    _user_token = f"{rng.getrandbits(64):016x}"
    admin_token = f"{rng.getrandbits(64):016x}"
    if request.get("mode") == "health":
        return "OK"
    if request.get("token") == admin_token:
        return "ADMIN_SESSION"
    return "DENIED"
