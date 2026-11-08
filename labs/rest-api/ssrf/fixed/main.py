import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

class Target(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'PUBLIC' if self.path == '/public' else b'LAB_INTERNAL_SECRET')
    def log_message(self, *args):
        pass

def run(request):
    # A loopback-only target replaces external services for a reproducible SSRF test.
    with HTTPServer(('127.0.0.1', 0), Target) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            path = request['path']
            if path != '/public':
                return 'DENIED'
            url = 'http://127.0.0.1:' + str(server.server_port) + path
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            with opener.open(url, timeout=2) as response:
                return response.read(1024).decode()
        finally:
            server.shutdown()
            thread.join()
