def run(document):
    messages = [{'role': 'system', 'content': 'Audit the code.'}]
    messages.append({'role': document.get('role', 'user'), 'content': document['content']})
    return [message['role'] for message in messages]
