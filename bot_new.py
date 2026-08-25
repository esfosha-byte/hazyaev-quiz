import os
import sys
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


PORT = int(os.environ.get("PORT", 10000))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def start_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    print(f"Health server started on port {PORT}")
    server.serve_forever()


print("Starting Telegram bot...")

bot_process = subprocess.Popen(
    [sys.executable, "bot.py"]
)

web_thread = threading.Thread(
    target=start_web_server,
    daemon=True
)
web_thread.start()

print("Telegram bot process started.")

try:
    bot_process.wait()
except KeyboardInterrupt:
    bot_process.terminate()
