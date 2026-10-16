def run(request):
    return {'Access-Control-Allow-Origin': request['origin'], 'Access-Control-Allow-Credentials': 'true'}
