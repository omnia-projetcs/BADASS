def run(request):
    profile = {'display_name': 'Alice', 'role': 'user'}
    profile.update(request)
    return profile
