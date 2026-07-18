from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from ourui.pipeline import compile_dump
from ourui.runtime import OurUIRequestHandler
from ourui.runtime.hmr import HmrHub
from ourui.runtime.invoke import _MODULE_CACHE, load_source_module

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "routes.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    _MODULE_CACHE.clear()


def test_dump_registers_routes() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 30
    routes = doc["semantic_graph"]["routes"]
    assert routes["/"] == "n0001"
    assert routes["/about"] == "n0003"
    assert len(routes) == 2


def test_http_serve_both_routes() -> None:
    _MODULE_CACHE.clear()
    load_source_module(FIXTURE.resolve())
    hmr = HmrHub(FIXTURE.resolve())
    hmr._loaded_generation = hmr.generation  # noqa: SLF001
    handler = type(
        "Bound",
        (OurUIRequestHandler,),
        {"source": FIXTURE.resolve(), "title": "routes-test", "hmr": hmr},
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)

        conn.request("GET", "/")
        res = conn.getresponse()
        home_body = res.read().decode("utf-8")
        assert res.status == 200
        assert "Welcome home" in home_body
        assert "Learn more about OurUI" not in home_body

        conn.request("GET", "/about")
        res = conn.getresponse()
        about_body = res.read().decode("utf-8")
        assert res.status == 200
        assert "Learn more about OurUI" in about_body
        assert "Welcome home" not in about_body

        conn.request("GET", "/missing")
        res = conn.getresponse()
        missing = json.loads(res.read().decode("utf-8"))
        assert res.status == 404
        assert missing["error"] == "not found"
        conn.close()
    finally:
        hmr.stop()
        httpd.shutdown()
        httpd.server_close()
