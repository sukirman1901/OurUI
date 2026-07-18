from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from ourui.emit.js import emit_js
from ourui.pipeline import compile_to_rtr, emit_html
from ourui.runtime.invoke import invoke_handler
from ourui.runtime import OurUIRequestHandler
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_invoke_server_handler() -> None:
    result = invoke_handler(FIXTURE, "get_started")
    assert result == {"message": "Welcome from OurUI server"}


def test_js_shim_posts_to_rpc() -> None:
    rtr = compile_to_rtr(FIXTURE)["rtr"].to_dict()
    js = emit_js(rtr)
    assert "/__ourui/call/" in js
    assert "fetch(" in js
    assert "get_started" in js


def test_emit_includes_rpc_shim() -> None:
    html = emit_html(FIXTURE)
    assert "data-ourui-on-click=\"get_started\"" in html
    assert "/__ourui/call/" in html


def test_http_serve_get_and_call() -> None:
    handler = type(
        "Bound",
        (OurUIRequestHandler,),
        {"source": FIXTURE.resolve(), "title": "test"},
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        body = res.read().decode("utf-8")
        assert res.status == 200
        assert "<button" in body

        conn.request(
            "POST",
            "/__ourui/call/get_started",
            body="{}",
            headers={"Content-Type": "application/json"},
        )
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        assert res.status == 200
        assert data["ok"] is True
        assert data["result"]["message"] == "Welcome from OurUI server"
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
