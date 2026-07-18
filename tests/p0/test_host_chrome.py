"""Host emit chrome defaults — package craft regressions (not landing-specific)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def _emit(tmp_path: Path, source: str) -> str:
    src = tmp_path / "app.py"
    src.write_text(source, encoding="utf-8")
    return emit_html(src, title="host")


def test_document_reset_and_root_bleed(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Hero(title="Hi"))
""",
    )
    assert "html, body {" in html
    assert "margin: 0;" in html
    assert "overflow-x: clip;" in html
    assert 'class="ourui-root"' in html


def test_theme_toggle_is_ghost_not_primary_fill(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Nav(actions=[ui.ThemeToggle()]), ui.Button("Go", color="primary"))
""",
    )
    assert 'class="ourui-theme-toggle"' in html
    assert "ourui-theme-toggle ourui-control" not in html
    assert "button.ourui-theme-toggle" in html
    assert "background: transparent;" in html
    assert 'data-reicon="sun"' in html
    assert 'data-reicon="moon-stars"' in html
    assert 'data-weight="filled"' in html
    assert ">Theme<" not in html
    assert "aria-label=" in html
    assert "html.dark button.ourui-theme-toggle .ourui-theme-icon-moon" in html


def test_nav_links_quiet_chrome(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Nav(
        brand=ui.Link("Brand", href="/"),
        items=[ui.Link("Docs", href="#")],
        actions=[ui.Link("Go", href="#", color="primary")],
        menu="drawer",
    )
)
""",
    )
    assert ".ourui-nav a.ourui-link:hover" in html
    assert ".ourui-nav-items a.ourui-link:not(.ourui-tone-primary)" in html
    assert 'class="ourui-nav-menu-btn"' in html
    assert "ourui-nav-menu-btn ourui-control" not in html
    assert "min-height: 2.75rem;" in html


def test_hero_section_semantic_headings(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Hero(title="Hero"), ui.Section(title="Section", children=[ui.Text("Body")]))
""",
    )
    assert '<h1 data-slot="title">Hero</h1>' in html
    assert '<h2 data-slot="title">Section</h2>' in html


def test_product_nav_breakout_and_flush(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Nav(brand=ui.Link("App", href="/")), ui.Hero(title="Admin"))
""",
    )
    assert "data-recipe=" not in html
    assert 'class="ourui-root" data-page-bleed="1"' not in html
    assert '[data-role="page"]:has(> [data-role="nav"]:first-child)' in html
    assert "padding-block-start: 0;" in html
    assert "margin-left: -50vw;" in html


def test_full_width_primary_excludes_nav(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Button("Save", color="primary"))
""",
    )
    assert "[data-role=\"section\"] button.ourui-tone-primary" in html
    assert ".ourui-nav[data-menu=\"drawer\"]" in html
    # Global blunt rule removed
    assert "button.ourui-tone-primary,\n  a.ourui-link.ourui-tone-primary" not in html


def test_table_scroll_contract(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Table(columns=["a", "b"], rows=[{"a": "1", "b": "2"}]))
""",
    )
    assert "overflow-x: auto;" in html
    assert ".ourui-table" in html


def test_host_chrome_uses_tokens_not_magic_hex(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
theme = ui.Theme(page={"max_width": "none"})
page = ui.Page(ui.Nav(brand=ui.Link("App", href="/")), ui.Code("x = 1"), ui.Dialog(title="D", children=[ui.Text("ok")]))
""",
    )
    assert "padding-inline: var(--ourui-page-pad-inline, var(--ourui-space-2xl));" in html
    assert "background: #ffffff;" not in html
    assert "background: #0c0c0e;" not in html
    assert ".ourui-code" in html
    assert "background: var(--ourui-card);" in html
    assert "color-mix(in srgb, var(--ourui-fg) 40%, transparent)" in html
    assert "gap: 0 !important;" not in html
