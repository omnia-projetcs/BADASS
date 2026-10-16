def run(value):
    sessions = {value: 'anonymous'}
    sessions[value] = 'alice'
    return sessions.get('attacker-known-id') == 'alice'
