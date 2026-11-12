"""Document store login handler evaluating nested query operator dictionaries."""

DOCUMENTS = [
    {"user": "alice", "api_key": "LAB_ALICE_KEY", "role": "admin"},
    {"user": "bob", "api_key": "LAB_BOB_KEY", "role": "viewer"},
]


def match_field(actual, criterion):
    if isinstance(criterion, dict):
        if "$ne" in criterion:
            return actual != criterion["$ne"]
        if "$gt" in criterion:
            return str(actual) > str(criterion["$gt"])
    return actual == criterion


def run(request):
    for doc in DOCUMENTS:
        if match_field(doc["user"], request.get("user")) and match_field(doc["api_key"], request.get("api_key")):
            return {"authenticated": doc["user"], "role": doc["role"]}
    return "DENIED"
