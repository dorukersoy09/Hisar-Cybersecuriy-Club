#!/usr/bin/env python3
"""
Classroom phishing-awareness capture server.

Serves the demo login page over PLAIN HTTP and prints whatever the
"victim" types to the server console, so the class can see that data
sent over HTTP is readable by anyone in the middle. This same POST is
what you will also see inside Wireshark or mitmproxy (see CAPTURE.md).

  USE ONLY on your own device / your own network, in a lesson you are
  running, with FAKE / dummy credentials. Never collect anyone's real
  password. End the session with the debrief in TEACHER-SCRIPT.md.

Run:
    python3 capture_server.py
then open   http://<this-computer-ip>:8000/   on the student device.

Press Ctrl+C to stop. Nothing is written to disk; captured values are
only echoed to this console and vanish when you close it.
"""

import argparse
import datetime
import html
import http.server
import socket
from urllib.parse import parse_qs

PAGE_FILES = {"/", "/index.html", "/style.css", "/script.js"}

# Injected into index.html so the page POSTs back here over HTTP.
INJECT = b'<script>window.CAPTURE_ENDPOINT = "/login";</script>'


class Handler(http.server.SimpleHTTPRequestHandler):
    def _send_html(self, body: bytes, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            try:
                with open("index.html", "rb") as f:
                    page = f.read()
            except FileNotFoundError:
                self._send_html(b"index.html not found next to capture_server.py", 500)
                return
            # Enable capture mode by injecting the endpoint flag.
            page = page.replace(b"<script src=\"script.js\">", INJECT + b"<script src=\"script.js\">")
            self._send_html(page)
            return
        # style.css / script.js and anything else -> normal static serving.
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8", "replace")
        fields = parse_qs(raw)
        ident = (fields.get("identifier", [""])[0])
        pw = (fields.get("password", [""])[0])

        stamp = datetime.datetime.now().strftime("%H:%M:%S")
        client = self.client_address[0]
        print("\n" + "=" * 56)
        print(f"  CAPTURED over plain HTTP  @ {stamp}  from {client}")
        print("-" * 56)
        print(f"  raw body on the wire : {raw}")
        print(f"  username / email     : {ident}")
        print(f"  password             : {pw}")
        print("=" * 56 + "\n")

        reveal = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Captured</title>
<style>
  body{{font-family:system-ui,Arial,sans-serif;background:#111;color:#eee;
       display:flex;min-height:100vh;align-items:center;justify-content:center;
       margin:0;padding:24px;text-align:center}}
  .box{{max-width:520px}}
  h1{{color:#f87171;font-size:1.6rem}}
  code{{display:block;background:#000;color:#4ade80;padding:14px;border-radius:8px;
        margin:16px 0;font-size:1rem;word-break:break-all}}
  p{{line-height:1.5;color:#cbd5e1}}
</style></head><body><div class="box">
<h1>&#9888; That link just stole your login</h1>
<p>You sent this over HTTP. Anyone on the network read it instantly:</p>
<code>username: {html.escape(ident)}<br>password: {html.escape(pw)}</code>
<p>If this had been your real password, an attacker would now have it.
This was a demo on your teacher's network with fake details &mdash; but on a
real untrusted link, the result is exactly this. Never type real
credentials into a link you did not expect.</p>
</div></body></html>"""
        self._send_html(reveal.encode("utf-8"))

    def log_message(self, fmt, *args):
        # Keep the request line visible; it is part of the lesson.
        print(f"  [req] {self.address_string()} - {fmt % args}")


def local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def main():
    ap = argparse.ArgumentParser(description="Classroom HTTP capture demo server")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    print("=" * 60)
    print(" Classroom phishing-awareness capture server")
    print(" PLAIN HTTP - for teaching only")
    print("-" * 60)
    print(" * Dummy credentials only. Never real passwords.")
    print(" * Your own device / your own network only.")
    print(" * Always run the debrief afterwards.")
    print("-" * 60)
    print(f" Students open:  http://{local_ip()}:{args.port}/")
    print(f" Or on this PC:  http://localhost:{args.port}/")
    print(" Ctrl+C to stop.")
    print("=" * 60)

    server = http.server.HTTPServer(("0.0.0.0", args.port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
