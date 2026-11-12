"""GraphQL query executor enforcing maximum nesting depth and disabling introspection."""

MAX_DEPTH = 3
ALLOWED_FIELDS = {"name", "organization", "members"}


def measure_and_validate(selection, depth=1):
    if not isinstance(selection, dict) or not selection or depth > MAX_DEPTH:
        return False
    for key, sub in selection.items():
        if not isinstance(key, str) or key.startswith("__") or key not in ALLOWED_FIELDS:
            return False
        if isinstance(sub, dict):
            if not measure_and_validate(sub, depth + 1):
                return False
        elif sub is not True:
            return False
    return True


def resolve_node(selection, depth=1):
    if "organization" in selection and isinstance(selection["organization"], dict):
        return {"org": resolve_node(selection["organization"], depth + 1)}
    if "members" in selection and isinstance(selection["members"], dict):
        return {"members": resolve_node(selection["members"], depth + 1)}
    return {"name": "alice", "depth": depth}


def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    query = request.get("query")
    if not measure_and_validate(query):
        return "DENIED"
    return resolve_node(query)
