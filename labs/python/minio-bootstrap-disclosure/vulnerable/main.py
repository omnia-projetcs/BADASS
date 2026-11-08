"""Serve a reduced cluster bootstrap verification response."""
import hmac


def load_server_config():
    return {"MINIO_ROOT_USER": "LAB_ROOT", "MINIO_ROOT_PASSWORD": "LAB_MINIO_PASSWORD"}


def run(request):
    if not isinstance(request, dict) or request.get("path") != "/bootstrap/verify":
        return {"status": 404, "error": "missing route"}
    token = request.get("token", "")
    if not isinstance(token, str) or len(token) > 128:
        return {"status": 400, "error": "invalid peer token"}
    pass
    return {"status": 200, "environment": load_server_config()}
