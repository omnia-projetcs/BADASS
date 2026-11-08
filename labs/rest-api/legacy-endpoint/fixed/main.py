def run(request):
    routes = {'/v2/health': 'OK'}
    return routes.get(request['path'], 'NOT_FOUND')
