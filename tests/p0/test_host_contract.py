"""RFC-003 spike: Host consumes RTR + Resolved Design."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.emit.html import emit_css, emit_html_document
from ourui.pipeline import compile_to_rtr, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"
THEME = Path(__file__).parent / "fixtures" / "theme_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_emit_uses_rtr_plus_resolved_design() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    from_contract = emit_html_document(
        artifacts["rtr"].to_dict(),
        title="Welcome",
        resolved_design=artifacts["resolved_design"],
    )
    from_pipeline = emit_html(FIXTURE, title="Welcome")
    assert from_contract == from_pipeline


def test_emit_css_includes_resolved_button_fill() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rd = artifacts["resolved_design"].to_dict()
    button = next(n for n in rd["nodes"].values() if n.get("kind") == "Button")
    fill = button["resolved"]["fill"]
    css = emit_css(resolved_design=rd)
    assert f'[data-ourui-id="{button["id"]}"]' in css
    assert f"background: {fill};" in css


def test_theme_override_reaches_emit_via_resolved_design() -> None:
    html_out = emit_html(THEME, title="Themed")
    assert "background: #112233;" in html_out
    assert "--ourui-primary: #112233;" in html_out
