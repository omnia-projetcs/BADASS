def run(request):
    return len([{'id': 1}] * request['limit'])
