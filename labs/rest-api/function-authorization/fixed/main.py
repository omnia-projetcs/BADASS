def run(request):
    role = 'user'  # Trusted principal for this fixture.
    if request['action'] == 'health':
        return 'HEALTHY'
    if role != 'admin':
        return 'DENIED'
    return 'ALL_USERS_DELETED'
