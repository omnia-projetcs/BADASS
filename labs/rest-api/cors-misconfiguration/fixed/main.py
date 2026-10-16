def run(request):
    if request['origin'] != 'https://app.example.test':
        return {}
    return {'Access-Control-Allow-Origin': request['origin'], 'Access-Control-Allow-Credentials': 'true'}
