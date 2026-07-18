from __future__ import annotations

from pathlib import Path

import pytest

from ourui.lsp.completions import get_completions
from ourui.pipeline import compile_dump, emit_html
from ourui.theme import DEFAULT_LIGHT, apply_theme_overrides, default_tokens, emit_tokens_css

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"
THEME_FIXTURE = Path(__file__).parent / "fixtures" / "theme_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_default_tokens_emit_css() -> None:
    css = emit_tokens_css(default_tokens())
    assert ":root {" in css
    assert ".dark {" in css
    assert "--ourui-primary:" in css
    assert "--ourui-bg:" in css
    assert "oklch" not in css
    assert DEFAULT_LIGHT["primary"] in css


def test_dump_includes_tokens() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 9
    assert doc["emit"]["tokens"] is True
    tokens = doc["semantic_graph"]["tokens"]
    assert tokens["light"]["primary"] == "#1a5f4a"
    assert tokens["light"]["primary_fg"] == "#f5faf8"
    assert "bg" in tokens["dark"]


def test_emit_html_uses_css_vars() -> None:
    html = emit_html(FIXTURE)
    assert "--ourui-primary:" in html
    assert ".dark {" in html
    assert "ourui-tone-primary" in html
    assert "var(--ourui-border)" in html
    assert "#d4d4d8" not in html


def test_theme_override_fixture() -> None:
    doc = compile_dump(THEME_FIXTURE)
    assert doc["semantic_graph"]["tokens"]["light"]["primary"] == "#112233"
    assert doc["semantic_graph"]["tokens"]["dark"]["primary"] == "#aabbcc"


def test_apply_theme_overrides_merge() -> None:
    base = default_tokens()
    out = apply_theme_overrides(base, light={"primary": "#000000"}, dark={"fg": "#eeeeee"})
    assert out["light"]["primary"] == "#000000"
    assert out["light"]["bg"] == base["light"]["bg"]
    assert out["dark"]["fg"] == "#eeeeee"


def test_lsp_color_token_completions() -> None:
    text = 'ui.Button("x", color="'
    items = get_completions(text, 0, len(text))
    labels = {i["label"] for i in items}
    assert "primary" in labels
    assert "danger" in labels


def test_lsp_theme_component() -> None:
    text = "ui.Th"
    items = get_completions(text, 0, len(text))
    labels = {i["label"] for i in items}
    assert "Theme" in labels
