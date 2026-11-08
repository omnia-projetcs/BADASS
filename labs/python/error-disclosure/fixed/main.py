def run(value):
    if value == 'ok':
        return 'OK'
    try:
        raise RuntimeError('db://admin:LAB_SECRET@database/internal')
    except RuntimeError:
        return 'Service unavailable'
