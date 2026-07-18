from __future__ import annotations

import json
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from ourui.pipeline import emit_html
from ourui.runtime.invoke import invoke_handler, load_source_module, snapshot_states


class OurUIRequestHandler(BaseHTTPRequestHandler):
    source: Path
    title: str

    def log_message(self, fmt: str, *args: Any) -> None:
        sys_stderr_write = __import__("sys").stderr.write
        sys_stderr_write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            module = load_source_module(self.source)
            state = snapshot_states(module)
            html = emit_html(self.source, title=self.title, state_values=state)
            self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")
            return
        self._send(404, b'{"error":"not found"}\n', "application/json")

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        prefix = "/__ourui/call/"
        if not path.startswith(prefix):
            self._send(404, b'{"error":"not found"}\n', "application/json")
            return
        name = path[len(prefix) :].strip("/")
        if not name or "/" in name:
            self._send(400, b'{"error":"invalid handler"}\n', "application/json")
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                payload = {}
        except json.JSONDecodeError:
            self._send(400, b'{"error":"invalid json"}\n', "application/json")
            return
        try:
            outcome = invoke_handler(self.source, name, payload)
            body = json.dumps(
                {
                    "ok": True,
                    "handler": name,
                    "result": outcome["result"],
                    "state": outcome["state"],
                },
                default=str,
            )
            self._send(200, (body + "\n").encode("utf-8"), "application/json")
        except KeyError as exc:
            body = json.dumps({"ok": False, "error": str(exc)})
            self._send(404, (body + "\n").encode("utf-8"), "application/json")
        except Exception as exc:  # noqa: BLE001
            body = json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
            )
            self._send(500, (body + "\n").encode("utf-8"), "application/json")


def serve(source: Path, *, host: str = "127.0.0.1", port: int = 8765, title: str | None = None) -> None:
    source = source.resolve()
    # Warm module cache so State persists across requests
    load_source_module(source)
    handler = type(
        "BoundOurUIHandler",
        (OurUIRequestHandler,),
        {"source": source, "title": title or source.stem},
    )
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"OurUI serve {source}")
    print(f"  http://{host}:{port}/")
    print("  POST /__ourui/call/<handler>")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
