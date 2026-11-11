def run(request):
    # Single-process simulation; production requires an atomic shared-store operation.
    if not isinstance(request, dict) or type(request.get("attempts")) is not int or request["attempts"] < 0:
        return 0
    reservations = 0
    for _ in range(min(request["attempts"], 100)):
        if reservations >= 2:
            break
        reservations += 1
    return reservations
