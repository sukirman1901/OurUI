from __future__ import annotations

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from ourui.runtime import OurUIRequestHandler
from ourui.runtime.invoke import _MODULE_CACHE, _STATE_DEFAULTS
from ourui.runtime.session import COOKIE_NAME, SessionStore

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "prod_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    _MODULE_CACHE.clear()
    _STATE_DEFAULTS.clear()


def _start_prod_server() -> tuple[ThreadingHTTPServer, int, SessionStore]:
    sessions = SessionStore()
    handler = type(
        "BoundProd",
        (OurUIRequestHandler,),
        {
            "source": FIXTURE.resolve(),
            "title": "prod-test",
            "hmr": None,
            "prod": True,
            "sessions": sessions,
        },
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port, sessions


def _cookie_from_response(res) -> str | None:
    # http.client may expose getheader
    raw = res.getheader("Set-Cookie")
    if not raw:
        return None
    for part in raw.split(";"):
        part = part.strip()
        if part.startswith(COOKIE_NAME + "="):
            return part
    return None


def test_health_prod() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/__ourui/health")
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        assert res.status == 200
        assert data["ok"] is True
        assert data["mode"] == "prod"
        assert data["store"] == "memory"
        assert data["workers"] == 1
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_rpc_500_hides_traceback() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request(
            "POST",
            "/__ourui/call/boom",
            body="{}",
            headers={"Content-Type": "application/json"},
        )
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        assert res.status == 500
        assert data["ok"] is False
        assert "traceback" not in data
        assert "intentional failure" in data["error"]
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_session_isolation() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        a = HTTPConnection("127.0.0.1", port, timeout=5)
        a.request("GET", "/")
        res_a = a.getresponse()
        assert res_a.status == 200
        body_a = res_a.read().decode("utf-8")
        assert "EventSource" not in body_a
        cookie_a = _cookie_from_response(res_a)
        assert cookie_a is not None

        a.request(
            "POST",
            "/__ourui/call/increment",
            body="{}",
            headers={"Content-Type": "application/json", "Cookie": cookie_a},
        )
        res_a2 = a.getresponse()
        data_a = json.loads(res_a2.read().decode("utf-8"))
        assert data_a["state"]["count"] == 1

        b = HTTPConnection("127.0.0.1", port, timeout=5)
        b.request("GET", "/")
        res_b = b.getresponse()
        cookie_b = _cookie_from_response(res_b)
        assert cookie_b is not None
        assert cookie_b != cookie_a
        res_b.read()

        b.request(
            "POST",
            "/__ourui/call/increment",
            body="{}",
            headers={"Content-Type": "application/json", "Cookie": cookie_b},
        )
        res_b2 = b.getresponse()
        data_b = json.loads(res_b2.read().decode("utf-8"))
        assert data_b["state"]["count"] == 1

        a.request(
            "POST",
            "/__ourui/call/increment",
            body="{}",
            headers={"Content-Type": "application/json", "Cookie": cookie_a},
        )
        res_a3 = a.getresponse()
        data_a3 = json.loads(res_a3.read().decode("utf-8"))
        assert data_a3["state"]["count"] == 2

        a.close()
        b.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_concurrent_invokes_smoke() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        cookie = _cookie_from_response(res)
        res.read()
        conn.close()
        assert cookie is not None

        def once(_: int) -> int:
            c = HTTPConnection("127.0.0.1", port, timeout=5)
            c.request(
                "POST",
                "/__ourui/call/increment",
                body="{}",
                headers={"Content-Type": "application/json", "Cookie": cookie},
            )
            r = c.getresponse()
            data = json.loads(r.read().decode("utf-8"))
            c.close()
            assert data["ok"] is True
            return int(data["result"])

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(once, range(20)))
        assert len(results) == 20
        assert max(results) == 20
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_prod_unknown_page_html_404() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/missing")
        res = conn.getresponse()
        body = res.read().decode("utf-8")
        assert res.status == 404
        assert "404" in body
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
