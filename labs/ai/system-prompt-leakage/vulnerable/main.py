def run(request):
    return 'LAB_INTERNAL_PROMPT' if request == 'debug' else 'READY'
