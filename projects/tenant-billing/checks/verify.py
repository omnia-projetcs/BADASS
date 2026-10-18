"""Trusted HTTP/SQL observations. Never copied into the application's image."""
import concurrent.futures
import hashlib
import hmac
import http.cookiejar
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import psycopg
import redis

VARIANT = sys.argv[1]
assert VARIANT in {"vulnerable", "fixed"}
BASE = "http://web:8000"
RESULTS = []


class Client:
    def __init__(self, username=None):
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.csrf = ""
        if username:
            _, session = self.request("GET", "/api/session/")
            self.csrf = session["csrf"]
            status, session = self.request("POST", "/api/session/", {
                "username": username, "password": "Lab-only-password-42"})
            assert status == 200, (status, session)
            self.csrf = session["csrf"]

    def request(self, method, path, data=None, headers=None):
        payload = None if data is None else json.dumps(data).encode()
        req = urllib.request.Request(BASE + path, data=payload, method=method, headers={
            "Content-Type": "application/json", "X-CSRFToken": self.csrf, **(headers or {})})
        try:
            response = self.opener.open(req, timeout=8)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            raw = response.read().decode()
            try:
                value = json.loads(raw)
            except ValueError:
                value = raw
            return response.status, value


def sql(query, params=()):
    with psycopg.connect(host="db", dbname="billing", user="billing", password=os.environ["LAB_DB_PASSWORD"]) as db:
        return db.execute(query, params).fetchall()


def reset():
    for command in (["flush", "--noinput"], ["seed"]):
        subprocess.run([sys.executable, "manage.py", *command], check=True, capture_output=True, timeout=30)
    redis.Redis(host="cache", db=0).flushdb()
    redis.Redis(host="cache", db=1).flushdb()


def expect(actual, vulnerable, fixed):
    expected = vulnerable if VARIANT == "vulnerable" else fixed
    assert actual == expected, {"actual": actual, "expected": expected}


def record(case, name, kind, callback):
    started = time.monotonic()
    try:
        reset()
        callback()
        RESULTS.append({"case_id": "tenant-billing/" + case, "name": name, "kind": kind, "status": "pass"})
    except Exception as error:
        RESULTS.append({"case_id": "tenant-billing/" + case, "name": name, "kind": kind,
                        "status": "fail", "error": repr(error)})
    RESULTS[-1]["duration_seconds"] = round(time.monotonic() - started, 3)


def finish_job(client, job_id):
    # The worker is a separate process, started after queuing/revocation. This
    # supplies deterministic scheduling without sleeps inside candidate code.
    with open("/tmp/worker.log", "w+") as log:
        worker = subprocess.Popen([sys.executable, "manage.py", "worker"], stdout=log, stderr=log)
        try:
            deadline = time.monotonic() + 12
            while time.monotonic() < deadline:
                status, job = client.request("GET", f"/api/exports/{job_id}/")
                assert status == 200, (status, job)
                if job["status"] != "queued":
                    return job
                if worker.poll() is not None:
                    break
                time.sleep(0.05)
            log.seek(0)
            raise AssertionError("Worker did not finish: " + log.read()[-2000:])
        finally:
            worker.terminate()
            try:
                worker.wait(timeout=3)
            except subprocess.TimeoutExpired:
                worker.kill()
                worker.wait()


def cache_benign():
    alice = Client("alice")
    for _ in range(2):
        status, invoice = alice.request("GET", "/api/tenants/1/invoices/INV-001/")
        assert status == 200 and invoice["customer"] == "ALPHA_CUSTOMER"


def cache_attack():
    bob, alice = Client("bob"), Client("alice")
    assert bob.request("GET", "/api/tenants/2/invoices/INV-001/")[1]["customer"] == "BETA_PRIVATE_CUSTOMER"
    status, invoice = alice.request("GET", "/api/tenants/1/invoices/INV-001/")
    assert status == 200
    expect(invoice["customer"], "BETA_PRIVATE_CUSTOMER", "ALPHA_CUSTOMER")


def cross_tenant_denied():
    assert Client("alice").request("GET", "/api/tenants/2/invoices/INV-001/")[0] == 403
    assert Client().request("GET", "/api/tenants/1/invoices/INV-001/")[0] == 401


def export_job(number, user="alice", revoke=False):
    client = Client(user)
    status, created = client.request("POST", "/api/tenants/1/exports/", {"numbers": [number]})
    assert status == 202
    if revoke:
        assert Client("alice").request("POST", f"/api/tenants/1/members/{user}/revoke/", {})[0] == 200
    job = finish_job(client, created["id"])
    observed = sql("SELECT status, content FROM billing_export WHERE id=%s", [created["id"]])[0]
    assert observed == (job["status"], job["content"])
    return job


def export_benign():
    job = export_job("INV-002")
    assert job["status"] == "ready" and "ALPHA_SECOND_CUSTOMER" in job["content"]
    assert "BETA_PRIVATE_CUSTOMER" not in job["content"]


def export_scope_attack():
    job = export_job("INV-001")
    assert job["status"] == "ready" and "ALPHA_CUSTOMER" in job["content"]
    expect("BETA_PRIVATE_CUSTOMER" in job["content"], True, False)


def export_revoke_attack():
    job = export_job("INV-002", user="eve", revoke=True)
    expect(job["status"], "ready", "denied")
    expect("ALPHA_SECOND_CUSTOMER" in job["content"], True, False)


def export_invalid():
    alice = Client("alice")
    assert alice.request("POST", "/api/tenants/1/exports/", {"numbers": "INV-001"})[0] == 400
    assert alice.request("POST", "/api/tenants/2/exports/", {"numbers": ["INV-001"]})[0] == 403
    assert sql("SELECT COUNT(*) FROM billing_export")[0][0] == 0


def invitation(revoke=False, wrong_user=False):
    alice, guest = Client("alice"), Client("bob" if wrong_user else "guest")
    status, invite = alice.request("POST", "/api/tenants/1/invitations/", {"email": "guest@example.test"})
    assert status == 201
    if revoke:
        assert alice.request("POST", f"/api/tenants/1/invitations/{invite['id']}/revoke/", {})[0] == 200
    status, _ = guest.request("POST", "/api/invitations/accept/", {"token": invite["token"]})
    if wrong_user:
        assert status == 403
    elif revoke:
        expect(status, 200, 403)
        count = sql("SELECT COUNT(*) FROM billing_membership m JOIN auth_user u ON u.id=m.user_id WHERE u.username='guest' AND m.active")[0][0]
        expect(count, 1, 0)
        expect(guest.request("GET", "/api/tenants/1/invoices/INV-002/")[0], 200, 403)
    else:
        assert status == 200
        assert guest.request("GET", "/api/tenants/1/invoices/INV-002/")[0] == 200
        assert guest.request("POST", "/api/invitations/accept/", {"token": invite["token"]})[0] == 403


def download(revoke=False, tamper=False):
    eve = Client("eve")
    status, data = eve.request("POST", "/api/tenants/1/invoices/INV-002/download/", {})
    assert status == 200
    if revoke:
        assert Client("alice").request("POST", "/api/tenants/1/members/eve/revoke/", {})[0] == 200
    token = data["token"] + ("tampered" if tamper else "")
    status, content = eve.request("GET", "/api/download/?" + urllib.parse.urlencode({"token": token}))
    if tamper:
        assert status == 400
    elif revoke:
        expect(status, 200, 403)
        expect("ALPHA_SECOND_CUSTOMER" in str(content), True, False)
    else:
        assert status == 200 and "ALPHA_SECOND_CUSTOMER" in content
        assert Client("bob").request("GET", "/api/download/?" + urllib.parse.urlencode({"token": token}))[0] == 403


def payment(repeat=False, concurrent=False, invalid=False):
    event = {"event_id": "lab-payment-1", "invoice": 1, "amount": 1000}
    signature = hmac.new(os.environ["LAB_WEBHOOK_KEY"].encode(), json.dumps(event).encode(), hashlib.sha256).hexdigest()
    if invalid:
        signature = "0" * 64
    def send():
        return Client().request("POST", "/api/webhooks/payment/", event, {"X-Signature": signature})[0]
    if concurrent:
        with concurrent_futures_pool() as pool:
            statuses = list(pool.map(lambda _: send(), range(2)))
    else:
        statuses = [send() for _ in range(2 if repeat else 1)]
    assert statuses == [403 if invalid else 200] * len(statuses)
    paid = sql("SELECT paid FROM billing_invoice WHERE id=1")[0][0]
    expect(paid, 0 if invalid else 1000 * len(statuses), 0 if invalid else 1000)
    assert sql("SELECT COUNT(*) FROM billing_paymentevent")[0][0] == (0 if invalid else 1)


def concurrent_futures_pool():
    return concurrent.futures.ThreadPoolExecutor(max_workers=2)


record("cache-isolation", "same-tenant cached reads", "benign", cache_benign)
record("cache-isolation", "cross-tenant cache collision", "attack", cache_attack)
record("cache-isolation", "authentication and direct authorization", "robustness", cross_tenant_denied)
record("export-scope", "single-tenant export", "benign", export_benign)
record("export-scope", "shared invoice reference in worker", "attack", export_scope_attack)
record("export-scope", "invalid or unauthorized submission", "robustness", export_invalid)
record("export-revocation", "active member export", "benign", export_benign)
record("export-revocation", "revoke before worker starts", "attack", export_revoke_attack)
record("export-revocation", "invalid or unauthorized submission", "robustness", export_invalid)
record("invitation-revocation", "valid invitation and one-time use", "benign", invitation)
record("invitation-revocation", "signed but revoked invitation", "attack", lambda: invitation(revoke=True))
record("invitation-revocation", "recipient mismatch", "robustness", lambda: invitation(wrong_user=True))
record("download-revocation", "active recipient download", "benign", download)
record("download-revocation", "signed link after membership revocation", "attack", lambda: download(revoke=True))
record("download-revocation", "signature tampering", "robustness", lambda: download(tamper=True))
record("webhook-replay", "single signed payment", "benign", payment)
record("webhook-replay", "sequential duplicate delivery", "attack", lambda: payment(repeat=True))
record("webhook-replay", "concurrent duplicate delivery", "attack", lambda: payment(concurrent=True))
record("webhook-replay", "invalid signature has no database effects", "robustness", lambda: payment(invalid=True))
print("BADASS_RESULT=" + json.dumps({"variant": VARIANT, "checks": RESULTS}))
sys.exit(0 if RESULTS and all(r["status"] == "pass" for r in RESULTS) else 1)
