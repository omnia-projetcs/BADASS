def run(request):
    # Single-process simulation; production requires an atomic shared-store operation.
    reservations = 0
    for _ in range(min(request['attempts'], 100)):
        if reservations >= 2:
            break
        reservations += 1
    return reservations
