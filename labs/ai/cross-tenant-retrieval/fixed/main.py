def run(query):
    docs = [{'tenant': 'alice', 'text': 'ALICE_PUBLIC'}, {'tenant': 'bob', 'text': 'BOB_PRIVATE'}]
    principal_tenant = 'alice'
    return [d['text'] for d in docs if d['tenant'] == principal_tenant and query in d['text']]
