import threading
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Every service in this fixture binds loopback; no external URL is accepted.
PATHS = {
    "public": "/public",
    "redirect-public": "/redirect-public",
    "redirect-private": "/redirect-private",
    "redirect-loop": "/redirect-loop",
}

class Target(BaseHTTPRequestHandler):
    def do_GET(self):
        with Path("http-access.log").open("a", encoding="utf-8") as stream:
            stream.write(self.path + "\n")
        redirects = {
            "/redirect-public": "/public",
            "/redirect-private": "/internal",
            "/redirect-loop": "/redirect-loop",
        }
        if self.path in redirects:
            self.send_response(302)
            self.send_header("Location", redirects[self.path])
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"PUBLIC" if self.path == "/public" else b"LAB_INTERNAL_SECRET")

    def log_message(self, *args):
        pass

def fetch(url, port):
    # Deliberate weakness: the first hop is allowlisted, redirected targets are not.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(url, timeout=2) as response:
            return response.read(1024).decode("utf-8")
    except urllib.error.HTTPError:
        return "FETCH_ERROR"


def run(request):
    Path("http-access.log").write_text("", encoding="utf-8")
    if not isinstance(request, dict) or request.get("resource") not in PATHS:
        return "DENIED"
    with HTTPServer(("127.0.0.1", 0), Target) as server:
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}" + PATHS[request["resource"]]
            return fetch(url, server.server_port)
        finally:
            server.shutdown()
            thread.join(timeout=2)
