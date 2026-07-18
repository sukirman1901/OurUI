from __future__ import annotations

import json
import multiprocessing as mp
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
from pathlib import Path

from ourui.runtime import serve
from ourui.runtime.session import COOKIE_NAME, FileSessionStore, make_session_store

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "prod_app.py"


def test_file_session_store_roundtrip(tmp_path: Path) -> None:
    store = FileSessionStore(tmp_path)
    sid, values, created = store.get_or_create(None)
    assert created
    assert values == {}
    store.set(sid, {"count": 3})
    assert store.get(sid) == {"count": 3}
    sid2, values2, created2 = store.get_or_create(sid)
    assert not created2
    assert sid2 == sid
    assert values2["count"] == 3


def test_file_session_concurrent_json_intact(tmp_path: Path) -> None:
    store = FileSessionStore(tmp_path)
    sid, _, _ = store.get_or_create(None)
    store.set(sid, {"count": 0})

    def bump(_: int) -> None:
        for _ in range(20):
            current = store.get(sid)
            store.set(sid, {"count": int(current.get("count", 0)) + 1})

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(bump, range(8)))
    raw = (tmp_path / f"{sid}.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, dict)
    assert "count" in data


def test_file_session_atomic_increment(tmp_path: Path) -> None:
    store = FileSessionStore(tmp_path)
    sid, _, _ = store.get_or_create(None)
    store.set(sid, {"count": 0})
    gate = threading.Lock()

    def bump(_: int) -> None:
        with gate:
            current = store.get(sid)
            store.set(sid, {"count": int(current.get("count", 0)) + 1})

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(bump, range(50)))
    assert store.get(sid)["count"] == 50


def test_make_session_store_rules(tmp_path: Path) -> None:
    mem = make_session_store(workers=1, session_dir=None, env={})
    assert type(mem).__name__ == "SessionStore"
    file_store = make_session_store(workers=2, session_dir=None, env={"TMPDIR": str(tmp_path)})
    assert isinstance(file_store, FileSessionStore)
    explicit = make_session_store(workers=1, session_dir=tmp_path / "sess", env={})
    assert isinstance(explicit, FileSessionStore)


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _serve_entry(source: str, port: int, session_dir: str) -> None:
    serve(
        Path(source),
        host="127.0.0.1",
        port=port,
        prod=True,
        workers=2,
        session_dir=Path(session_dir),
        title="mw",
    )


def test_multi_worker_health_and_session(tmp_path: Path) -> None:
    session_dir = tmp_path / "sessions"
    port = _free_port()
    ctx = mp.get_context("spawn")
    proc = ctx.Process(
        target=_serve_entry,
        args=(str(FIXTURE.resolve()), port, str(session_dir)),
    )
    proc.start()
    try:
        health = None
        for _ in range(80):
            try:
                conn = HTTPConnection("127.0.0.1", port, timeout=1)
                conn.request("GET", "/__ourui/health")
                res = conn.getresponse()
                health = json.loads(res.read().decode("utf-8"))
                conn.close()
                if res.status == 200:
                    break
            except OSError:
                time.sleep(0.1)
        assert health is not None
        assert health["ok"] is True
        assert health["mode"] == "prod"
        assert health["workers"] == 2
        assert health["store"] == "file"

        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        assert res.status == 200
        cookie = res.getheader("Set-Cookie")
        res.read()
        assert cookie and COOKIE_NAME in cookie

        conn.request(
            "POST",
            "/__ourui/call/increment",
            body="{}",
            headers={"Content-Type": "application/json", "Cookie": cookie.split(";")[0]},
        )
        res2 = conn.getresponse()
        data = json.loads(res2.read().decode("utf-8"))
        assert data["ok"] is True
        assert data["state"]["count"] == 1
        conn.close()

        assert list(session_dir.glob("*.json"))
    finally:
        proc.terminate()
        proc.join(timeout=5)
        if proc.is_alive():
            proc.kill()
            proc.join(timeout=2)
