def run(request):
    if not isinstance(request, dict) or not isinstance(request.get("id"), str):
        return {"status": 400}
    invoices = {"1": {"owner": "alice", "total": 10}, "2": {"owner": "bob", "total": 900}}
    invoice = invoices.get(request["id"])
    if not invoice or invoice["owner"] != "alice":
        return {"status": 404}
    return {"status": 200, "body": invoice}
