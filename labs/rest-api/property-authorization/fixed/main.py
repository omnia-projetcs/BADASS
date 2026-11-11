def run(request):
    profile = {"display_name": "Alice", "role": "user"}
    if isinstance(request, dict) and isinstance(request.get("display_name"), str):
        profile["display_name"] = request["display_name"]
    return profile
