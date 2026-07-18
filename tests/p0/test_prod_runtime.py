from __future__ import annotations

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from ourui.runtime import OurUIRequestHandler
from ourui.runtime.invoke import _MODULE_CACHE, _STATE_DEFAULTS
from ourui.runtime.security import CSRF_HEADER, RateLimiter
from ourui.runtime.session import COOKIE_NAME, SessionStore

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "prod_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    _MODULE_CACHE.clear()
    _STATE_DEFAULTS.clear()


def _start_prod_server(*, rate_limit: int | None = None) -> tuple[ThreadingHTTPServer, int, SessionStore]:
    sessions = SessionStore()
    limiter = RateLimiter(limit=rate_limit) if rate_limit is not None else RateLimiter(limit=0)
    handler = type(
        "BoundProd",
        (OurUIRequestHandler,),
        {
            "source": FIXTURE.resolve(),
            "title": "prod-test",
            "hmr": None,
            "prod": True,
            "sessions": sessions,
            "rate_limiter": limiter,
        },
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, port, sessions


def _cookie_from_response(res) -> str | None:
    raw = res.getheader("Set-Cookie")
    if not raw:
        return None
    for part in raw.split(";"):
        part = part.strip()
        if part.startswith(COOKIE_NAME + "="):
            return part
    return None


def _csrf_from_html(html: str) -> str:
    match = re.search(r'name="ourui-csrf" content="([^"]+)"', html)
    assert match is not None, "missing csrf meta"
    return match.group(1)


def _session_from_get(port: int) -> tuple[str, str]:
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("GET", "/")
    res = conn.getresponse()
    assert res.status == 200
    html = res.read().decode("utf-8")
    cookie = _cookie_from_response(res)
    conn.close()
    assert cookie is not None
    return cookie, _csrf_from_html(html)


def _rpc(
    port: int,
    handler: str,
    *,
    cookie: str | None = None,
    csrf: str | None = None,
    body: dict | None = None,
) -> tuple[int, dict]:
    payload = dict(body or {})
    headers = {"Content-Type": "application/json"}
    if cookie:
        headers["Cookie"] = cookie
    if csrf:
        headers[CSRF_HEADER] = csrf
        payload["_csrf"] = csrf
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request(
        "POST",
        f"/__ourui/call/{handler}",
        body=json.dumps(payload),
        headers=headers,
    )
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    status = res.status
    conn.close()
    return status, data


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
        assert res.getheader("X-Content-Type-Options") == "nosniff"
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_rpc_requires_session() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        status, data = _rpc(port, "increment")
        assert status == 401
        assert data["ok"] is False
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_rpc_requires_csrf() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        cookie, _csrf = _session_from_get(port)
        status, data = _rpc(port, "increment", cookie=cookie)
        assert status == 403
        assert "csrf" in data["error"]
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_rpc_500_hides_details() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        cookie, csrf = _session_from_get(port)
        status, data = _rpc(port, "boom", cookie=cookie, csrf=csrf)
        assert status == 500
        assert data["ok"] is False
        assert data["error"] == "internal server error"
        assert "traceback" not in data
        assert "intentional" not in data["error"]
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_session_isolation() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        cookie_a, csrf_a = _session_from_get(port)
        status, data_a = _rpc(port, "increment", cookie=cookie_a, csrf=csrf_a)
        assert status == 200
        assert data_a["state"]["count"] == 1

        cookie_b, csrf_b = _session_from_get(port)
        assert cookie_b != cookie_a
        status, data_b = _rpc(port, "increment", cookie=cookie_b, csrf=csrf_b)
        assert status == 200
        assert data_b["state"]["count"] == 1

        status, data_a3 = _rpc(port, "increment", cookie=cookie_a, csrf=csrf_a)
        assert status == 200
        assert data_a3["state"]["count"] == 2
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_concurrent_invokes_smoke() -> None:
    httpd, port, _ = _start_prod_server(rate_limit=0)
    try:
        cookie, csrf = _session_from_get(port)

        def once(_: int) -> int:
            status, data = _rpc(port, "increment", cookie=cookie, csrf=csrf)
            assert status == 200
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


def test_prod_html_has_csrf_and_nonce() -> None:
    httpd, port, _ = _start_prod_server()
    try:
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        html = res.read().decode("utf-8")
        assert res.status == 200
        assert 'name="ourui-csrf"' in html
        assert "nonce=" in html
        assert "nonce-" in html  # CSP directive
        cookie = res.getheader("Set-Cookie") or ""
        assert "HttpOnly" in cookie
        assert "SameSite=Lax" in cookie
        conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
