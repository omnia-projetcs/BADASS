def run(request):
    if not isinstance(request, dict) or request.get("origin") != "https://app.example.test":
        return {}
    return {"Access-Control-Allow-Origin": request["origin"], "Access-Control-Allow-Credentials": "true"}
