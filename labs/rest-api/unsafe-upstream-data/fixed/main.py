def run(request):
    if not isinstance(request, dict):
        return "DENIED"
    upstream = request.get("upstream")
    if not isinstance(upstream, dict):
        return "DENIED"
    price = upstream.get("price")
    if type(price) is not int or not 0 <= price <= 100:
        return "DENIED"
    return 100 - price
