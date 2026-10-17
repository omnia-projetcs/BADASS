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

class NoAutomaticRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, newurl):
        return None


def fetch(url, port):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoAutomaticRedirect())
    for _ in range(3):
        parsed = urllib.parse.urlsplit(url)
        # Revalidate every actual destination before making that request.
        if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1"
                or parsed.port != port or parsed.username is not None
                or parsed.password is not None or parsed.query or parsed.fragment
                or parsed.path not in set(PATHS.values())):
            return "DENIED"
        try:
            with opener.open(url, timeout=2) as response:
                return response.read(1024).decode("utf-8")
        except urllib.error.HTTPError as error:
            try:
                if error.code not in {301, 302, 303, 307, 308}:
                    return "FETCH_ERROR"
                location = error.headers.get("Location")
                if not location:
                    return "DENIED"
                url = urllib.parse.urljoin(url, location)
            finally:
                error.close()
    return "DENIED"


def run(request):
    Path("http-access.log").write_text("", encoding="utf-8")
    if not isinstance(request, dict) or not isinstance(request.get("resource"), str):
        return "DENIED"
    if request["resource"] not in PATHS:
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
