"""Phase S3–S6: tokens, ThemeToggle, Footer, layout, motion, Canvas, polish."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, compile_to_rtr, emit_html
from ourui.theme import TOKEN_KEYS, default_tokens, emit_tokens_css

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "s3_s6_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_token_keys_include_type_space_elevation() -> None:
    for key in (
        "font_sans",
        "font_display",
        "text_xs",
        "text_2xl",
        "space_xs",
        "space_2xl",
        "elev_0",
        "elev_3",
        "leading_normal",
    ):
        assert key in TOKEN_KEYS
    css = emit_tokens_css(default_tokens())
    assert "--ourui-font-display:" in css
    assert "--ourui-elev-2:" in css
    assert "--ourui-space-xl:" in css


def test_dump_s3_s6_kinds() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 30
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    for kind in (
        "ThemeToggle",
        "Footer",
        "Canvas",
        "Image",
        "Icon",
        "Meta",
        "Code",
        "CopyButton",
        "Menu",
    ):
        assert kind in kinds


def test_emit_theme_toggle_and_tokens() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert "data-ourui-theme-toggle" in html_out
    assert "--ourui-font-sans:" in html_out
    assert "--ourui-elev-1:" in html_out
    assert "toggleTheme" in html_out or "data-ourui-theme-toggle" in html_out
    assert 'classList.toggle("dark")' in html_out


def test_emit_footer_hero_pad() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert "<footer" in html_out
    assert "ourui-footer" in html_out
    assert "ourui-pad-xl" in html_out or 'data-role="hero"' in html_out


def test_emit_layout_intents() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert "ourui-shell-split-sidebar" in html_out
    assert "ourui-gap-lg" in html_out
    assert "ourui-align-center" in html_out


def test_emit_motion() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert "ourui-motion-reveal-fade-up" in html_out
    assert "ourui-motion-reveal-mask-wipe" in html_out
    assert "--ourui-motion-ease:" in html_out
    assert "prefers-reduced-motion" in html_out


def test_emit_canvas_plasma() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert "data-ourui-canvas" in html_out
    assert "Plasma.init" in html_out
    assert '"mode":"gradient"' in html_out or "gradient" in html_out


def test_emit_s6_polish() -> None:
    html_out = emit_html(FIXTURE, title="S3-S6")
    assert 'name="description"' in html_out
    assert "property=\"og:title\"" in html_out or "og:title" in html_out
    assert "data-ourui-copy" in html_out
    assert "data-reicon=" in html_out
    assert "<img" in html_out
    assert "ourui-code" in html_out
    assert "data-menu=\"drawer\"" in html_out
    assert "data-ourui-drawer" in html_out
    assert "data-ourui-menu" in html_out
    assert 'aria-invalid="true"' in html_out


def test_rtr_roles() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rtr = artifacts["rtr"].to_dict()
    roles = {n.get("attributes", {}).get("role") for n in rtr["nodes"].values()}
    assert "theme-toggle" in roles
    assert "footer" in roles
    assert "canvas" in roles
    assert "meta" in roles
