"""GraphQL query executor without depth limits or introspection restrictions."""

SCHEMA_TYPES = ["Query", "User", "Organization", "InternalSecret"]


def resolve_node(selection, depth=1):
    if "__schema" in selection:
        return {"types": SCHEMA_TYPES, "depth": depth}
    if "organization" in selection and isinstance(selection["organization"], dict):
        return {"org": resolve_node(selection["organization"], depth + 1)}
    if "members" in selection and isinstance(selection["members"], dict):
        return {"members": resolve_node(selection["members"], depth + 1)}
    return {"name": "alice", "depth": depth}


def run(request):
    query = request.get("query", {})
    return resolve_node(query)
