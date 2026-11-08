"""Scope cached responses to the authenticated tenant and local document identifier."""
from copy import deepcopy


SESSIONS = {"LAB_NORTH_SESSION": "north", "LAB_SOUTH_SESSION": "south"}
DOCUMENTS = {("north", "summary"): "LAB_NORTH_PRIVATE_SUMMARY",
             ("south", "summary"): "LAB_SOUTH_PRIVATE_SUMMARY",
             ("north", "invoice"): "LAB_NORTH_INVOICE",
             ("south", "invoice"): "LAB_SOUTH_INVOICE"}


def fetch(request, cache):
    if not isinstance(request, dict):
        return {"status": 400}
    token = request.get("session")
    if not isinstance(token, str) or token not in SESSIONS:
        return {"status": 401}
    tenant = SESSIONS[token]
    document_id = request.get("document_id")
    if not isinstance(document_id, str) or not 1 <= len(document_id) <= 64:
        return {"status": 400}
    # Cache scope matches the authenticated origin lookup scope.
    key = (tenant, document_id)
    if key in cache:
        return deepcopy(cache[key])
    content = DOCUMENTS.get((tenant, document_id))
    if content is None:
        return {"status": 404}
    response = {"status": 200, "content": content}
    cache[key] = deepcopy(response)
    return response


def run(request):
    if (not isinstance(request, dict) or not isinstance(request.get("requests"), list)
            or not 1 <= len(request["requests"]) <= 8):
        return {"status": 400}
    # Successive requests share one actual cache; each invocation starts fresh.
    cache = {}
    return {"responses": [fetch(item, cache) for item in request["requests"]]}
