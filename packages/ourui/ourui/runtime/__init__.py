from __future__ import annotations

import json
import multiprocessing as mp
import os
import socket
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from ourui.analysis import build_semantic_graph
from ourui.pipeline import emit_html
from ourui.runtime.hmr import HmrHub
from ourui.runtime.invoke import (
    _INVOKE_LOCK,
    _MODULE_CACHE,
    apply_states,
    invoke_handler,
    load_source_module,
    snapshot_states,
)
from ourui.runtime.session import (
    SessionStoreProtocol,
    make_session_store,
    parse_sid_cookie,
    set_cookie_header,
)


class OurUIRequestHandler(BaseHTTPRequestHandler):
    source: Path
    title: str
    hmr: HmrHub | None = None
    prod: bool = False
    sessions: SessionStoreProtocol | None = None
    workers: int = 1
    store_kind: str = "memory"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(
        self,
        code: int,
        body: bytes,
        content_type: str,
        *,
        extra_headers: list[tuple[str, str]] | None = None,
    ) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for key, value in extra_headers:
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _cookie_headers(self, sid: str, created: bool) -> list[tuple[str, str]]:
        if self.prod and created:
            return [("Set-Cookie", set_cookie_header(sid))]
        return []

    def _session(self) -> tuple[str | None, dict[str, Any], bool]:
        if not self.prod or self.sessions is None:
            return None, {}, False
        raw = parse_sid_cookie(self.headers.get("Cookie"))
        sid, values, created = self.sessions.get_or_create(raw)
        return sid, values, created

    def _reload_if_stale(self) -> None:
        """Drop cached module when HMR generation advances after a file edit."""
        if self.hmr is None:
            return
        key = self.source.resolve().as_posix()
        snap = self.hmr.snapshot()
        token = snap["generation"]
        cached = getattr(self.hmr, "_loaded_generation", -1)
        if token != cached:
            _MODULE_CACHE.pop(key, None)
            load_source_module(self.source, reload=True)
            self.hmr._loaded_generation = token  # noqa: SLF001 — serve-local marker

    def _match_page_route(self, path: str) -> str | None:
        sg, _ = build_semantic_graph(self.source)
        if path == "/index.html":
            path = "/"
        if path in sg.routes:
            return path
        return None

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/__ourui/health":
            mode = "prod" if self.prod else "dev"
            body = json.dumps(
                {
                    "ok": True,
                    "mode": mode,
                    "workers": self.workers,
                    "store": self.store_kind,
                    "pid": os.getpid(),
                }
            ) + "\n"
            self._send(200, body.encode("utf-8"), "application/json")
            return
        if path == "/__ourui/hmr":
            if self.prod or self.hmr is None:
                self._send(404, b'{"error":"not found"}\n', "application/json")
                return
            self._sse_loop()
            return
        if path == "/__ourui/hmr/status":
            if self.prod or self.hmr is None:
                self._send(404, b'{"error":"not found"}\n', "application/json")
                return
            body = json.dumps(self.hmr.snapshot()) + "\n"
            self._send(200, body.encode("utf-8"), "application/json")
            return
        route = self._match_page_route(path)
        if route is not None:
            self._reload_if_stale()
            sid, session_values, created = self._session()
            if self.prod:
                with _INVOKE_LOCK:
                    module = load_source_module(self.source)
                    apply_states(module, session_values, path=self.source)
                    state = snapshot_states(module)
                    if sid is not None and self.sessions is not None:
                        if created or not session_values:
                            self.sessions.set(sid, state)
                            state = self.sessions.get(sid)
                html = emit_html(
                    self.source,
                    title=self.title,
                    route=route,
                    state_values=state,
                    hmr=False,
                )
                headers = self._cookie_headers(sid or "", created) if sid else []
                self._send(200, html.encode("utf-8"), "text/html; charset=utf-8", extra_headers=headers)
                return
            module = load_source_module(self.source)
            state = snapshot_states(module)
            html = emit_html(
                self.source,
                title=self.title,
                route=route,
                state_values=state,
                hmr=True,
            )
            self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")
            return
        if self.prod and not path.startswith("/__ourui/"):
            self._send(404, b"<h1>404 Not Found</h1>\n", "text/html; charset=utf-8")
            return
        self._send(404, b'{"error":"not found"}\n', "application/json")

    def _sse_loop(self) -> None:
        assert self.hmr is not None
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        gen = self.hmr.generation
        try:
            self.wfile.write(b"event: hello\ndata: ok\n\n")
            self.wfile.flush()
            while True:
                new_gen = self.hmr.wait_changed(gen, timeout=15.0)
                if new_gen != gen:
                    gen = new_gen
                    payload = json.dumps({"generation": gen})
                    self.wfile.write(f"event: reload\ndata: {payload}\n\n".encode())
                    self.wfile.flush()
                else:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        prefix = "/__ourui/call/"
        if not path.startswith(prefix):
            self._send(404, b'{"error":"not found"}\n', "application/json")
            return
        self._reload_if_stale()
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
        sid: str | None = None
        created = False
        try:
            if self.prod and self.sessions is not None:
                with _INVOKE_LOCK:
                    cookie_raw = parse_sid_cookie(self.headers.get("Cookie"))
                    sid, session_values, created = self.sessions.get_or_create(cookie_raw)
                    outcome = invoke_handler(
                        self.source,
                        name,
                        payload,
                        state_values=session_values,
                        use_lock=False,
                    )
                    self.sessions.set(sid, outcome["state"])
            else:
                outcome = invoke_handler(self.source, name, payload, use_lock=True)
            body = json.dumps(
                {
                    "ok": True,
                    "handler": name,
                    "result": outcome["result"],
                    "state": outcome["state"],
                },
                default=str,
            )
            headers = self._cookie_headers(sid or "", created) if sid else []
            self._send(
                200,
                (body + "\n").encode("utf-8"),
                "application/json",
                extra_headers=headers,
            )
        except KeyError as exc:
            body = json.dumps({"ok": False, "error": str(exc)})
            self._send(404, (body + "\n").encode("utf-8"), "application/json")
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(traceback.format_exc() + "\n")
            err: dict[str, Any] = {"ok": False, "error": str(exc)}
            if not self.prod:
                err["traceback"] = traceback.format_exc()
            self._send(500, (json.dumps(err) + "\n").encode("utf-8"), "application/json")


class _SharedSocketHTTPServer(ThreadingHTTPServer):
    """HTTP server that uses a pre-bound listening socket (multi-worker)."""

    def server_bind(self) -> None:  # noqa: D102
        pass

    def server_activate(self) -> None:  # noqa: D102
        pass


def _bind_handler(
    source: Path,
    title: str,
    *,
    prod: bool,
    sessions: SessionStoreProtocol | None,
    hmr: HmrHub | None,
    workers: int,
    store_kind: str,
) -> type[OurUIRequestHandler]:
    return type(
        "BoundOurUIHandler",
        (OurUIRequestHandler,),
        {
            "source": source,
            "title": title,
            "hmr": hmr,
            "prod": prod,
            "sessions": sessions,
            "workers": workers,
            "store_kind": store_kind,
        },
    )


def _worker_serve(
    sock: socket.socket,
    source: Path,
    title: str,
    sessions: SessionStoreProtocol,
    workers: int,
    store_kind: str,
) -> None:
    load_source_module(source)
    handler = _bind_handler(
        source,
        title,
        prod=True,
        sessions=sessions,
        hmr=None,
        workers=workers,
        store_kind=store_kind,
    )
    httpd = _SharedSocketHTTPServer(("127.0.0.1", 0), handler, bind_and_activate=False)
    httpd.socket = sock
    httpd.server_address = sock.getsockname()  # type: ignore[assignment]
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


def _print_banner(
    source: Path,
    host: str,
    port: int,
    *,
    prod: bool,
    workers: int,
    store_kind: str,
    session_dir: Path | None,
) -> None:
    sg, _ = build_semantic_graph(source)
    mode = "prod" if prod else "dev"
    print(f"OurUI serve ({mode}) workers={workers} store={store_kind} {source}")
    if session_dir is not None:
        print(f"  session-dir {session_dir}")
    if sg.routes:
        for route_path in sorted(sg.routes):
            print(f"  http://{host}:{port}{route_path}")
    else:
        print(f"  http://{host}:{port}/")
    print("  POST /__ourui/call/<handler>")
    print("  GET  /__ourui/health")
    if not prod:
        print("  GET  /__ourui/hmr  (SSE reload)")


def serve(
    source: Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    title: str | None = None,
    prod: bool = False,
    workers: int = 1,
    session_dir: Path | None = None,
) -> None:
    source = source.resolve()
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if workers > 1 and not prod:
        raise ValueError("--workers > 1 requires --prod")

    display_title = title or source.stem
    sessions: SessionStoreProtocol | None = None
    hmr: HmrHub | None = None
    store_kind = "memory"
    resolved_session_dir: Path | None = None

    if prod:
        sessions = make_session_store(workers=workers, session_dir=session_dir)
        from ourui.runtime.session import FileSessionStore

        if isinstance(sessions, FileSessionStore):
            store_kind = "file"
            resolved_session_dir = sessions.directory
        load_source_module(source)
    else:
        hmr = HmrHub(source)
        load_source_module(source)
        hmr._loaded_generation = hmr.generation  # noqa: SLF001

    _print_banner(
        source,
        host,
        port,
        prod=prod,
        workers=workers,
        store_kind=store_kind,
        session_dir=resolved_session_dir,
    )

    if workers == 1:
        handler = _bind_handler(
            source,
            display_title,
            prod=prod,
            sessions=sessions,
            hmr=hmr,
            workers=1,
            store_kind=store_kind,
        )
        httpd = ThreadingHTTPServer((host, port), handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            if hmr is not None:
                hmr.stop()
            httpd.server_close()
        return

    assert sessions is not None
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(128)
    sock.set_inheritable(True)

    ctx = mp.get_context("fork")
    procs: list[mp.Process] = []
    try:
        for _ in range(workers):
            proc = ctx.Process(
                target=_worker_serve,
                args=(sock, source, display_title, sessions, workers, store_kind),
                daemon=False,
            )
            proc.start()
            procs.append(proc)
        for proc in procs:
            proc.join()
    except KeyboardInterrupt:
        print("\nStopped.")
        for proc in procs:
            proc.terminate()
        for proc in procs:
            proc.join(timeout=2.0)
    finally:
        sock.close()
