"""Named packs + recipes (A+B catalog)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.design import list_packs, list_recipes, materialize_pack
from ourui.design.packs import PACKS, RECIPES
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_pack_catalog_anti_slop() -> None:
    assert list_packs() == ["ourui-console", "ourui-default", "ourui-editorial"]
    assert list_recipes() == ["console", "editorial", "marketing", "ops", "product"]
    # No purple / cream brochure tells in shipped packs
    for pid, pack in PACKS.items():
        light = pack["modes"]["light"]
        joined = " ".join(light.values()).lower()
        assert "7c3aed" not in joined
        assert "6366f1" not in joined
        assert "f4f1ea" not in joined
        assert "fraunces" not in joined
        assert light["radius"] in {"0", "0.25rem", "0.375rem"}
        assert "IBM Plex Sans" in light["font_sans"]


def test_recipe_ops_compacts_and_widens(tmp_path: Path) -> None:
    src = tmp_path / "ops.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(recipe="ops")
page = ui.Page(ui.Hero(title="Ops"), ui.Button("Go", color="primary"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    rd = doc["resolved_design"]
    assert doc["version"] == 30
    assert doc["emit"]["recipes"] is True
    assert rd["pack"] == "ourui-default"
    assert rd["recipe"] == "ops"
    assert rd["density"] == "compact"
    assert rd["page"]["max_width"] == "72rem"
    html = emit_html(src, title="ops")
    assert "ourui-density-compact" in html
    assert "--ourui-page-max-width: 72rem" in html


def test_pack_editorial_sharp_radius(tmp_path: Path) -> None:
    src = tmp_path / "ed.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(pack="ourui-editorial")
page = ui.Page(ui.Hero(title="Read"), ui.Button("Next"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    rd = doc["resolved_design"]
    assert rd["pack"] == "ourui-editorial"
    assert rd.get("recipe") is None
    assert rd["tokens"]["light"]["radius"] == "0"
    assert rd["page"]["max_width"] == "36rem"
    html = emit_html(src, title="ed")
    assert "--ourui-page-max-width: 36rem" in html
    assert "--ourui-radius: 0;" in html


def test_recipe_console(tmp_path: Path) -> None:
    src = tmp_path / "con.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(recipe="console", accent="#0e7490")
page = ui.Page(ui.Button("Run", color="accent"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    rd = doc["resolved_design"]
    assert rd["pack"] == "ourui-console"
    assert rd["recipe"] == "console"
    assert rd["density"] == "compact"
    assert rd["tokens"]["light"]["accent"] == "#0e7490"


def test_unknown_recipe_diagnostic(tmp_path: Path) -> None:
    src = tmp_path / "bad.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(recipe="neon-disco")
page = ui.Page(ui.Button("X"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    codes = {d["code"] for d in doc["diagnostics"]}
    assert "E_THEME" in codes


def test_materialize_recipe_page_merge() -> None:
    pack = materialize_pack(recipe_id="ops")
    assert pack["id"] == "ourui-default"
    assert pack["page"]["max_width"] == "72rem"
    assert pack["density"]["default"] == "compact"
    assert pack["recipe"] == "ops"
    assert "product" in RECIPES


def test_recipe_marketing_full_bleed(tmp_path: Path) -> None:
    src = tmp_path / "mkt.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(recipe="marketing")
page = ui.Page(
    ui.Nav(brand=ui.Link("OurUI", href="/"), items=[ui.Link("Docs", href="#")]),
    ui.Hero(title="Ship intent", subtitle="Compiler writes the rest"),
    ui.Section(title="Next", children=[ui.Text("Body")]),
)
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    rd = doc["resolved_design"]
    assert rd["recipe"] == "marketing"
    assert rd["page"]["max_width"] == "none"
    assert rd["pack_version"] == "1.2.0"
    html = emit_html(src, title="mkt")
    assert 'data-recipe="marketing"' in html
    assert "--ourui-page-max-width: none" in html
    assert 'data-role="nav"' in html
    assert "<h1 data-slot=\"title\">Ship intent</h1>" in html
    assert "<h2 data-slot=\"title\">Next</h2>" in html
    assert "text-decoration: underline" in html  # focus / prose still have underline rules
    assert ".ourui-nav a.ourui-link:hover" in html
    assert "a.ourui-link.ourui-tone-primary" in html
