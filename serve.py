#!/usr/bin/env python3
"""Serve Golf Shot Tracker over HTTP/HTTPS for local and phone testing."""

from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT = ROOT / ".local-dev-cert.pem"
KEY = ROOT / ".local-dev-key.pem"


def local_ips():
    ips = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
    except OSError:
        pass
    return ips


def ensure_cert():
    if CERT.exists() and KEY.exists():
        return
    print("Generating self-signed certificate (one-time)...")
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(KEY), "-out", str(CERT),
            "-days", "3650", "-nodes",
            "-subj", "/CN=golf-tracker.local/O=Local Dev/C=NZ",
        ],
        check=True,
        cwd=ROOT,
    )


def main():
    parser = argparse.ArgumentParser(description="Serve Golf Shot Tracker")
    parser.add_argument("--port", type=int, default=8443)
    parser.add_argument(
        "--http-only", action="store_true",
        help="HTTP only (GPS on phone will not work over LAN)",
    )
    args = parser.parse_args()
    os.chdir(ROOT)

    from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

    class Handler(SimpleHTTPRequestHandler):
        extensions_map = {
            **SimpleHTTPRequestHandler.extensions_map,
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
        }

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    scheme = "http"

    if not args.http_only:
        ensure_cert()
        import ssl
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(str(CERT), str(KEY))
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        scheme = "https"

    print()
    print("Golf Shot Tracker - dev server")
    print("=" * 40)
    print("On this computer:")
    print("  %s://localhost:%s/" % (scheme, args.port))
    print("  %s://127.0.0.1:%s/" % (scheme, args.port))
    for ip in local_ips():
        print("On phone (same Wi-Fi): %s://%s:%s/" % (scheme, ip, args.port))
    if scheme == "https":
        print()
        print("On phone: accept the certificate warning once, then allow Location.")
    print()
    print("Press Ctrl+C to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
