def run(request):
    invoices = {'1': {'owner': 'alice', 'total': 10}, '2': {'owner': 'bob', 'total': 900}}
    return {'status': 200, 'body': invoices[request['id']]}
