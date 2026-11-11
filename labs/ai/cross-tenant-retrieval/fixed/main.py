"""Vector retrieval filter that scopes results to the authenticated caller's tenant."""


def run(query):
    if not isinstance(query, str):
        return []
    docs = [
        {"tenant": "alice", "text": "ALICE_PUBLIC"},
        {"tenant": "bob", "text": "BOB_PRIVATE"},
    ]
    principal_tenant = "alice"
    return [d["text"] for d in docs if d["tenant"] == principal_tenant and query in d["text"]]
