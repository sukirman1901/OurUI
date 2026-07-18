"""Theme page= / density — no packs or recipes."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.cli import main as cli_main
from ourui.design.resolve import DEFAULT_PAGE
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_default_page_measure() -> None:
    assert DEFAULT_PAGE["max_width"] == "42rem"


def test_recipe_rejected(tmp_path: Path) -> None:
    src = tmp_path / "r.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(recipe="marketing")
page = ui.Page(ui.Hero(title="X"))
""",
        encoding="utf-8",
    )
    assert cli_main(["check", str(src)]) == 1
    with pytest.raises(ValueError, match="E_THEME"):
        emit_html(src, title="x")


def test_pack_rejected(tmp_path: Path) -> None:
    src = tmp_path / "p.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(pack="ourui-default")
page = ui.Page(ui.Hero(title="X"))
""",
        encoding="utf-8",
    )
    assert cli_main(["check", str(src)]) == 1
    with pytest.raises(ValueError, match="E_THEME"):
        emit_html(src, title="x")


def test_page_bleed_via_theme_page(tmp_path: Path) -> None:
    src = tmp_path / "bleed.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(page={"max_width": "none", "pad_block": "0", "pad_inline": "0"})
page = ui.Page(ui.Nav(brand=ui.Link("A", href="/")), ui.Hero(title="H"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    rd = doc["resolved_design"]
    assert rd["page"]["max_width"] == "none"
    assert "pack" not in rd
    assert "pack_version" not in rd
    html = emit_html(src, title="bleed")
    assert 'data-page-bleed="1"' in html


def test_density_still_works(tmp_path: Path) -> None:
    src = tmp_path / "d.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(density="compact")
page = ui.Page(ui.Hero(title="D"), ui.Button("Ok", color="primary"))
""",
        encoding="utf-8",
    )
    html = emit_html(src, title="d")
    assert "ourui-density-compact" in html
