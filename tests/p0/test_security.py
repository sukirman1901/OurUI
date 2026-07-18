from __future__ import annotations

import hashlib
from pathlib import Path

from ourui.diagnostics import collect_enterprise_diagnostics
from ourui.pipeline import DUMP_SCHEMA_VERSION, compile_dump, emit_html
from ourui.runtime.security import (
    RateLimiter,
    cookie_secure_enabled,
    csp_content,
    new_csrf_token,
    validate_csrf,
)
from ourui.runtime.session import (
    SessionStore,
    ensure_csrf,
    normalize_envelope,
    session_state,
    set_cookie_header,
    with_state,
)
from ourui.serialize import dumps_deterministic

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "prod_app.py"
FRAME = Path(__file__).parent / "fixtures" / "textarea_frame_app.py"


def test_schema_28_attestation_sha256() -> None:
    dump = compile_dump(FIXTURE)
    assert dump["version"] == 28
    assert DUMP_SCHEMA_VERSION == 28
    att = dump["attestation"]
    assert att["schema"] == 28
    assert isinstance(att["sha256"], str) and len(att["sha256"]) == 64
    body = dict(dump)
    body["attestation"] = {k: v for k, v in att.items() if k != "sha256"}
    expected = hashlib.sha256(dumps_deterministic(body).encode("utf-8")).hexdigest()
    assert att["sha256"] == expected
    assert dump["emit"]["csrf"] is True
    assert dump["emit"]["security_headers"] is True


def test_csrf_helpers() -> None:
    token = new_csrf_token()
    assert validate_csrf(token, token)
    assert not validate_csrf(token, "nope")
    assert not validate_csrf(None, token)


def test_session_envelope() -> None:
    store = SessionStore()
    sid, env, created = store.get_or_create(None)
    assert created
    assert "state" in env and "csrf" in env
    assert session_state(env) == {}
    env2, csrf = ensure_csrf(env)
    store.set(sid, with_state(env2, {"count": 1}))
    got = store.get(sid)
    assert session_state(got)["count"] == 1
    assert got["csrf"] == csrf
    legacy = normalize_envelope({"count": 9})
    assert session_state(legacy)["count"] == 9


def test_cookie_secure_flag(monkeypatch) -> None:
    monkeypatch.delenv("OURUI_COOKIE_SECURE", raising=False)
    assert "Secure" not in set_cookie_header("abc")
    assert "Secure" in set_cookie_header("abc", secure=True)
    assert cookie_secure_enabled({"OURUI_COOKIE_SECURE": "1"})


def test_csp_nonce() -> None:
    plain = csp_content(nonce=None)
    assert "unsafe-inline" in plain
    nonced = csp_content(nonce="abc123")
    assert "nonce-abc123" in nonced
    assert "unsafe-inline" not in nonced.split("script-src")[1].split(";")[0]


def test_rate_limiter() -> None:
    lim = RateLimiter(limit=2, window_s=60.0)
    assert lim.allow("a")
    assert lim.allow("a")
    assert not lim.allow("a")
    assert lim.allow("b")


def test_emit_csrf_meta() -> None:
    html = emit_html(FIXTURE, title="sec", csrf_token="tok-1", csp_nonce="n1")
    assert 'name="ourui-csrf" content="tok-1"' in html
    assert 'nonce="n1"' in html
    assert "nonce-n1" in html


def test_sec001_frame_srcdoc() -> None:
    diags = collect_enterprise_diagnostics(FRAME)
    codes = {d.code for d in diags}
    assert "SEC001" in codes


def test_gateway_readme_exists() -> None:
    readme = ROOT / "examples" / "enterprise" / "gateway" / "README.md"
    assert readme.is_file()
    assert "OURUI_GATEWAY_TOKEN" in readme.read_text(encoding="utf-8")
