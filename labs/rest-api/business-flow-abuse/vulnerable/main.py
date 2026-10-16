def run(request):
    reservations = 0
    for _ in range(request['attempts']):
        reservations += 1
    return reservations
