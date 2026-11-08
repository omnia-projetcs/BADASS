def run(request):
    return 'HEALTHY' if request['action'] == 'health' else 'ALL_USERS_DELETED'
