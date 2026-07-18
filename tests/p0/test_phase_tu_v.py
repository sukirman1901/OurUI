"""Phase T–U surfaces + Phase V diagnostics/Derived."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.cli import main as cli_main
from ourui.diagnostics import collect_diagnostics
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "phase_tu_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_phase_tu_emit() -> None:
    html = emit_html(FIXTURE, title="tu")
    assert "<form" in html
    assert "data-ourui-on-submit" in html
    assert 'data-role="dialog"' in html
    assert 'data-role="toast"' in html
    assert "<ul" in html and "ourui-list" in html
    assert "<table" in html
    assert "ourui-empty" in html
    assert "ourui-spinner" in html
    assert "ourui-alert" in html
    assert "ourui-field-helper" in html


def test_phase_tu_dump_schema() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 25
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    assert {"Form", "Dialog", "Toast", "List", "Table", "Empty", "Spinner", "Alert"} <= kinds
    assert "label" in doc["derived"] or "label" in doc["semantic_graph"].get("derived", {})


def test_ourui_check_ok() -> None:
    assert cli_main(["check", str(FIXTURE)]) == 0


def test_collect_diagnostics_ok() -> None:
    diags = collect_diagnostics(FIXTURE)
    assert all(d.severity != "error" or d.code for d in diags)
