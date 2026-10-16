def run(request):
    return {'status': 200 if request.get('token') else 401}
