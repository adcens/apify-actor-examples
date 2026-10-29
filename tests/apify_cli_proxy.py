"""Maintainer test harness (not needed to use the examples).

A tiny local HTTP server that forwards Apify API calls through the Apify CLI (`apify api ...`),
so the examples can be tested against the live Actors using the CLI's own login: no API token is
read, printed or passed around by the test scripts. The examples' own Authorization header is ignored.

Run: python tests/apify_cli_proxy.py [port]   (needs `apify` on PATH and `apify login` done)
"""
import gzip
import json
import math
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qsl, urlsplit

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
LOG = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep stdout quiet
        pass

    def _forward(self, method):
        parts = urlsplit(self.path)
        path = parts.path
        params = dict(parse_qsl(parts.query))
        params.pop("token", None)
        body = b""
        if int(self.headers.get("Content-Length") or 0):
            body = self.rfile.read(int(self.headers["Content-Length"]))
            if self.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
        # Log streaming is not needed for tests: answer with an empty log.
        if re.search(r"/log$", path):
            return self._send(200, b"", "text/plain")
        if "waitForFinish" in params:  # keep each CLI call short; clients poll again
            params["waitForFinish"] = str(min(int(params["waitForFinish"]), 50))
        cmd = ["apify", "api", "-X", method, path.lstrip("/")]
        if params:
            cmd += ["-p", json.dumps(params)]
        if body:
            cmd += ["-d", body.decode("utf-8")]
        LOG.append(f"{method} {path}")
        if __import__("os").environ.get("PROXY_DEBUG"):
            print(method, path, params, flush=True)
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                              env={**__import__("os").environ, "APIFY_CLI_DISABLE_TELEMETRY": "1"})
        out = proc.stdout.strip()
        if proc.returncode != 0 or out.startswith("Error"):
            err = (out or proc.stderr).strip()
            m = re.search(r"Error: (\d{3})", err)
            code = int(m.group(1)) if m else 500
            j = err[err.find("{"):] if "{" in err else json.dumps({"error": {"type": "proxy-error", "message": err[:500]}})
            return self._send(code, j.encode(), "application/json")
        headers = {}
        if re.search(r"/datasets/[^/]+/items$", path) or path.endswith("/run-sync-get-dataset-items"):
            try:
                items = json.loads(out or "[]")
                n = len(items) if isinstance(items, list) else 0
                headers = {"X-Apify-Pagination-Total": str(int(params.get("offset", 0)) + n), "X-Apify-Pagination-Offset": params.get("offset", "0"),
                           "X-Apify-Pagination-Count": str(n), "X-Apify-Pagination-Limit": params.get("limit", str(max(n, 1))),
                           "X-Apify-Pagination-Desc": params.get("desc", "false")}
            except json.JSONDecodeError:
                pass
        status = 201 if method == "POST" and re.search(r"/runs$", path) else 200
        return self._send(status, (out or "{}").encode(), "application/json", headers)

    def _send(self, code, payload, ctype, headers=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        self._forward("GET")

    def do_POST(self):
        self._forward("POST")

    def do_PUT(self):
        self._forward("PUT")


if __name__ == "__main__":
    print(f"apify CLI proxy on http://127.0.0.1:{PORT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
