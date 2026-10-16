def run(request):
    price = request.get('upstream', {}).get('price')
    if type(price) is not int or not 0 <= price <= 100:
        return 'DENIED'
    return 100 - price
