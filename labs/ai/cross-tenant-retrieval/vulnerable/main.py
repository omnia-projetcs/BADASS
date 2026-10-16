def run(query):
    docs = [{'tenant': 'alice', 'text': 'ALICE_PUBLIC'}, {'tenant': 'bob', 'text': 'BOB_PRIVATE'}]
    return [d['text'] for d in docs if query in d['text']]
