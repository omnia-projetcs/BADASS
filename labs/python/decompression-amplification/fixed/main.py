"""Bound decompression output before allocation and publish only complete valid data."""
import base64
import binascii
import hashlib
from pathlib import Path
import zlib


MAX_COMPRESSED = 1024
MAX_OUTPUT = 1024


def unpack(packed):
    decoder = zlib.decompressobj()
    # One extra byte detects overflow without materializing the whole expansion.
    data = decoder.decompress(packed, MAX_OUTPUT + 1)
    if len(data) > MAX_OUTPUT:
        raise OverflowError("expanded data exceeds budget")
    if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError("expected one complete zlib stream")
    return data


def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    encoded = request.get("payload")
    if not isinstance(encoded, str) or len(encoded) > 1368:
        return {"status": 400}
    try:
        packed = base64.b64decode(encoded, validate=True)
        if len(packed) > MAX_COMPRESSED:
            return {"status": 400}
        data = unpack(packed)
    except OverflowError:
        return {"status": 413}
    except (ValueError, binascii.Error, zlib.error):
        return {"status": 400}
    Path("expanded.bin").write_bytes(data)
    return {"status": 201, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
