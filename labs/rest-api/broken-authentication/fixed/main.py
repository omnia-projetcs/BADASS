import hmac
def run(request):
    # Synthetic opaque token for the fixture, not a production credential store.
    token = request.get('token', '')
    valid = isinstance(token, str) and hmac.compare_digest(token, 'LAB_VALID_TOKEN')
    return {'status': 200 if valid else 401}
