from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from ourui.emit.js import emit_js
from ourui.pipeline import compile_to_rtr, emit_html
from ourui.runtime import OurUIRequestHandler
from ourui.runtime.hmr import HmrHub
from ourui.runtime.invoke import _MODULE_CACHE, _STATE_DEFAULTS, invoke_handler, load_source_module

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    _MODULE_CACHE.clear()
    _STATE_DEFAULTS.clear()


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
    assert "EventSource" not in js


def test_js_hmr_optional() -> None:
    rtr = compile_to_rtr(FIXTURE)["rtr"].to_dict()
    js = emit_js(rtr, hmr=True)
    assert "EventSource" in js
    assert "/__ourui/hmr" in js


def test_emit_includes_rpc_shim() -> None:
    html = emit_html(FIXTURE)
    assert 'data-ourui-on-click="get_started"' in html
    assert "/__ourui/call/" in html
    assert 'data-ourui-bind="count"' in html


def test_hmr_hub_detects_change(tmp_path: Path) -> None:
    src = tmp_path / "app.py"
    src.write_text("x = 1\n", encoding="utf-8")
    hub = HmrHub(src)
    time.sleep(0.05)
    before = hub.generation
    time.sleep(0.05)
    src.write_text("x = 2\n", encoding="utf-8")
    deadline = time.time() + 2.0
    while time.time() < deadline and hub.generation == before:
        time.sleep(0.05)
    assert hub.generation > before
    hub.stop()


def test_http_serve_get_and_call() -> None:
    _MODULE_CACHE.clear()
    load_source_module(FIXTURE.resolve())
    hmr = HmrHub(FIXTURE.resolve())
    hmr._loaded_generation = hmr.generation  # noqa: SLF001
    handler = type(
        "Bound",
        (OurUIRequestHandler,),
        {"source": FIXTURE.resolve(), "title": "test", "hmr": hmr, "prod": False, "sessions": None},
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
        assert "EventSource" in body

        conn.request("GET", "/__ourui/hmr/status")
        res = conn.getresponse()
        status = json.loads(res.read().decode("utf-8"))
        assert "generation" in status

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
        hmr.stop()
        httpd.shutdown()
        httpd.server_close()
