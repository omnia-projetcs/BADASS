import hmac
def run(request):
    # The test fixture stands in for a server-side session token.
    expected = 'lab-session-csrf-token'
    token = request.get('csrf', '')
    if not isinstance(token, str) or not hmac.compare_digest(token, expected):
        return 'DENIED'
    return 'TRANSFERRED'
