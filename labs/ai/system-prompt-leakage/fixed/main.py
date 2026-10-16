def run(request):
    return 'DENIED' if request == 'debug' else 'READY'
