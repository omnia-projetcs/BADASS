def run(code):
    namespace = {}
    exec(code, namespace)
    return namespace['RESULT']
