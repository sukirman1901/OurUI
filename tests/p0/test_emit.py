from __future__ import annotations

from pathlib import Path

import pytest

from ourui.emit.html import emit_html_document
from ourui.pipeline import compile_dump, compile_to_rtr, dump_json, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"
GOLDEN_HTML = Path(__file__).parent / "goldens" / "example.emit.html"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_emit_html_contains_host_mapping() -> None:
    html_out = emit_html(FIXTURE, title="Welcome")
    assert "<!DOCTYPE html>" in html_out
    assert "<main" in html_out
    assert "<header" in html_out
    assert "<button" in html_out
    assert "Get Started" in html_out
    assert 'data-ourui-on-click="get_started"' in html_out
    assert 'data-ourui-bind="count"' in html_out
    assert "ourui:call" in html_out
    assert "applyState" in html_out
    assert "<Hero" not in html_out


def test_emit_only_uses_rtr() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    from_rtr = emit_html_document(artifacts["rtr"].to_dict(), title="Welcome")
    from_pipeline = emit_html(FIXTURE, title="Welcome")
    assert from_rtr == from_pipeline


def test_emit_deterministic() -> None:
    assert emit_html(FIXTURE) == emit_html(FIXTURE)


def test_dump_version_notes_emit() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 10
    assert doc["emit"]["html"] is True
    assert doc["emit"]["js"] is True
    assert doc["emit"]["state"] is True


def test_golden_html() -> None:
    GOLDEN_HTML.parent.mkdir(parents=True, exist_ok=True)
    actual = emit_html(FIXTURE, title="example")
    if not GOLDEN_HTML.exists():
        GOLDEN_HTML.write_text(actual, encoding="utf-8")
    assert actual == GOLDEN_HTML.read_text(encoding="utf-8")


def test_dump_still_works() -> None:
    text = dump_json(FIXTURE)
    assert '"rtr"' in text
    assert "get_started" in text
