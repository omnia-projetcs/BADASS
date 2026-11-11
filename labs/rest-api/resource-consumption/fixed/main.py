def run(request):
    if not isinstance(request, dict):
        return {"status": 400}
    limit = request.get("limit")
    if type(limit) is not int or not 1 <= limit <= 100:
        return {"status": 400}
    return len([{"id": 1}] * limit)
