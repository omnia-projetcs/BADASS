def run(request):
    profile = {'display_name': 'Alice', 'role': 'user'}
    if 'display_name' in request:
        profile['display_name'] = request['display_name']
    return profile
