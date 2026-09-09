#!/usr/bin/env python3
"""dashboard_test_server.py -- a TEST RIG ONLY.  Not part of the dashboard.

the owner's page needs no server: dashboard.html reads the folder through the
File System Access API.  That API's folder dialog is a dialog of the
operating system, and no automation available here can click it, so the
live page cannot be driven end to end by a script.

This program exists so the live loader can still be MEASURED in a real
browser.  It serves the Research directory over http with BYTE RANGE
support, so the loader's prefix and tail slices fetch a few kilobytes of
a 331 MB file exactly as Blob.slice does off disk.  A shim in the page
(dashboard_test_shim.js) dresses those fetches as directory handles.

Nothing in dashboard.html, dashboard_join.js, dashboard_loader.js or
viewer_build.py knows this file exists.

    /tmp/reconnect_venv/bin/python3 dashboard_test_server.py <root> <port>
"""

import http.server
import os
import posixpath
import socketserver
import sys
import urllib.parse


class RangeHandler(http.server.SimpleHTTPRequestHandler):

    def translate_path(self, path):
        path = urllib.parse.urlparse(path).path
        path = urllib.parse.unquote(path)
        path = posixpath.normpath(path).lstrip("/")
        return os.path.join(self.directory, path)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Accept-Ranges", "bytes")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        rng = self.headers.get("Range")
        if not rng:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            self.send_error(404)
            return None
        size = os.path.getsize(path)
        spec = rng.split("=", 1)[1]
        first, _, last = spec.partition("-")
        start = int(first) if first else 0
        end = int(last) if last else size - 1
        end = min(end, size - 1)
        length = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(length))
        self.send_header("Content-Range",
                         "bytes %d-%d/%d" % (start, end, size))
        self.end_headers()
        with open(path, "rb") as fh:
            fh.seek(start)
            self.wfile.write(fh.read(length))
        return None

    def log_message(self, fmt, *args):
        return None


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    root = sys.argv[1]
    port = int(sys.argv[2])
    handler = lambda *a, **k: RangeHandler(*a, directory=root, **k)
    with Server(("127.0.0.1", port), handler) as srv:
        print("serving %s on http://127.0.0.1:%d" % (root, port))
        sys.stdout.flush()
        srv.serve_forever()


if __name__ == "__main__":
    main()
