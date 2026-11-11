def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("path"), str):
        return "NOT_FOUND"
    routes = {"/v2/health": "OK"}
    return routes.get(request["path"], "NOT_FOUND")
