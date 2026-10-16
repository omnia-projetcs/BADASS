import secrets
def run(value):
    sessions = {value: 'anonymous'}
    del sessions[value]
    sessions[secrets.token_urlsafe(32)] = 'alice'
    return sessions.get('attacker-known-id') == 'alice'
