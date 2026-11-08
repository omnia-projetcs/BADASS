def run(value):
    return {k: v for k, v in value.items() if k in {'event', 'user'}}
