def run(value):
    principal = 'alice'  # Established by the trusted authentication layer.
    if value != principal:
        return 'DENIED'
    return 'ALICE_DATA'
