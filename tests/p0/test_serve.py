from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from ourui.emit.js import emit_js
from ourui.pipeline import compile_to_rtr, emit_html
from ourui.runtime import OurUIRequestHandler
from ourui.runtime.invoke import _MODULE_CACHE, invoke_handler, load_source_module

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    _MODULE_CACHE.clear()


def test_invoke_server_handler() -> None:
    outcome = invoke_handler(FIXTURE, "get_started")
    assert outcome["result"] == {"message": "Welcome from OurUI server"}
    assert "count" in outcome["state"]


def test_state_persists_across_invokes() -> None:
    _MODULE_CACHE.clear()
    a = invoke_handler(FIXTURE, "increment")
    b = invoke_handler(FIXTURE, "increment")
    assert a["result"] == 1
    assert b["result"] == 2
    assert b["state"]["count"] == 2


def test_js_shim_posts_to_rpc() -> None:
    rtr = compile_to_rtr(FIXTURE)["rtr"].to_dict()
    js = emit_js(rtr)
    assert "/__ourui/call/" in js
    assert "fetch(" in js
    assert "applyState" in js


def test_emit_includes_rpc_shim() -> None:
    html = emit_html(FIXTURE)
    assert 'data-ourui-on-click="get_started"' in html
    assert "/__ourui/call/" in html
    assert 'data-ourui-bind="count"' in html


def test_http_serve_get_and_call() -> None:
    _MODULE_CACHE.clear()
    load_source_module(FIXTURE.resolve())
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
        assert 'data-ourui-bind="count"' in body

        conn.request(
            "POST",
            "/__ourui/call/increment",
            body="{}",
            headers={"Content-Type": "application/json"},
        )
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        assert res.status == 200
        assert data["ok"] is True
        assert data["result"] == 1
        assert data["state"]["count"] == 1
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
