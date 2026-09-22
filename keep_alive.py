import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"SPARK CTF BOT is alive")

    # Loglarni tinch tutamiz
    def log_message(self, *args):
        pass


def _serve():
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), _Handler)
    server.serve_forever()


def keep_alive():
    """Render/UptimeRobot uchun kichik HTTP server (alohida oqimda)."""
    threading.Thread(target=_serve, daemon=True).start()
