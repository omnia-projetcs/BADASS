def run(request):
    routes = {'/v2/health': 'OK', '/v1/debug/users': 'LAB_PRIVATE_USERS'}
    return routes.get(request['path'], 'NOT_FOUND')
