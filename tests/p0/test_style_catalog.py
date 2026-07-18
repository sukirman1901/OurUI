"""Style Intent Catalog (ADR-013) — scales, utilities, passthrough."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.design.scales import emit_scale_css_vars
from ourui.design.style_catalog import assert_catalog_complete, catalog_summary
from ourui.design.style_intents import emit_utility_css, style_intent_classes
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def _emit(tmp_path: Path, source: str) -> str:
    src = tmp_path / "app.py"
    src.write_text(source, encoding="utf-8")
    return emit_html(src, title="style")


def test_catalog_matrix_complete() -> None:
    assert_catalog_complete()
    summary = catalog_summary()
    assert summary["entries"] >= 80
    assert summary["by_status"].get("A", 0) > 0


def test_scale_and_utility_css_contain_core_tokens() -> None:
    scales = emit_scale_css_vars()
    assert "--ourui-size-lg:" in scales
    assert "--ourui-space-4:" in scales
    utils = emit_utility_css()
    assert ".ourui-w-lg {" in utils
    assert "width: var(--ourui-size-lg)" in utils
    assert ".ourui-pad-x-4 {" in utils
    assert ".ourui-grow-1 {" in utils
    assert ".ourui-grid-cols-3 {" in utils


def test_style_intent_classes_map_props() -> None:
    classes = style_intent_classes(
        {"width": "lg", "pad_x": "4", "grow": 1, "grid_cols": 3, "text": "Hello world"}
    )
    assert "ourui-w-lg" in classes
    assert "ourui-pad-x-4" in classes
    assert "ourui-grow-1" in classes
    assert "ourui-grid-cols-3" in classes
    # content text must not become font-size class
    assert "ourui-text-Hello-world" not in classes
    assert "ourui-text-Hello" not in classes

    type_classes = style_intent_classes({"text": "lg"})
    assert "ourui-text-lg" in type_classes


def test_emit_includes_scales_and_width_class(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Shell(
        ui.Text("Box"),
        width="lg",
        pad_x="4",
        grow="1",
        gap="md",
    )
)
""",
    )
    assert "--ourui-size-lg:" in html
    assert ".ourui-w-lg {" in html
    assert "ourui-w-lg" in html
    assert "ourui-pad-x-4" in html
    assert "ourui-grow-1" in html


def test_literal_width_inline_rule(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(ui.Shell(ui.Text("Lit"), width="12rem"))
""",
    )
    assert "width: 12rem;" in html
    assert "data-ourui-id=" in html


def test_theme_scale_override(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
theme = ui.Theme(sizes={"lg": "40rem"})
page = ui.Page(ui.Shell(ui.Text("T"), width="lg"))
""",
    )
    assert "--ourui-size-lg: 40rem;" in html


def test_table_columns_not_grid(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
page = ui.Page(
    ui.Table(columns=["Name", "Age"], rows=[["Ada", "36"]])
)
""",
    )
    assert "ourui-table" in html or "<table" in html
    assert "ourui-grid-cols-Name" not in html


def test_promoted_c_row_intents() -> None:
    classes = style_intent_classes(
        {
            "object_position": "center",
            "grid_auto_cols": "fr",
            "bg_size": "cover",
            "filter": "grayscale",
            "skew_x": 3,
            "text_columns": 2,
        }
    )
    assert "ourui-object-position-center" in classes
    assert "ourui-grid-auto-cols-fr" in classes
    assert "ourui-bg-size-cover" in classes
    assert "ourui-filter-grayscale" in classes
    assert "ourui-skew-x-3" in classes
    assert "ourui-text-columns-2" in classes
    utils = emit_utility_css()
    assert ".ourui-object-position-center {" in utils
    assert ".ourui-filter-grayscale {" in utils


def test_dump_includes_style_catalog(tmp_path: Path) -> None:
    src = tmp_path / "app.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(ui.Text("Hi"))
""",
        encoding="utf-8",
    )
    dump = compile_dump(src)
    assert dump["emit"].get("style_intents") is True
    assert dump["style_catalog"]["entries"] >= 80
