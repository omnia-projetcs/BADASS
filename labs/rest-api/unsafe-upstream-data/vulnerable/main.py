def run(request):
    return 100 - request['upstream']['price']
