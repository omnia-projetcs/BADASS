def run(value):
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items() if k in {'event', 'user'}}
