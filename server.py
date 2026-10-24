#!/usr/bin/env python3
"""
FirstPatch Local Web Server
Runs a lightweight, zero-dependency development server for FirstPatch.
Usage:
    python3 server.py [port]
"""

import http.server
import socketserver
import sys
import os
import socket

DEFAULT_PORT = 3000


class FirstPatchHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        sys.stderr.write(
            f"[{self.log_date_time_string()}] {format % args}\n"
        )


def find_open_port(start_port):
    port = start_port
    while port < start_port + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1
    return start_port


def run():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(target_dir)

    preferred_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    port = find_open_port(preferred_port)

    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", port), FirstPatchHandler) as httpd:
        print("=" * 60)
        print("  FirstPatch — Open-Source Contribution Finder")
        print("  Problem Statement #20 | Hacktoberfest Hack Day 2026")
        print("=" * 60)
        print(f"  Local URL:   http://localhost:{port}")
        print(f"  Network URL: http://127.0.0.1:{port}")
        print("=" * 60)
        print("  Press Ctrl+C to stop the server\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server... Goodbye!")
            sys.exit(0)


if __name__ == '__main__':
    run()
