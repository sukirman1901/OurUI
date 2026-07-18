"""Enterprise E1: Show/When + dynamic List/Table."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "e1_show_list_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_e1_dump_schema_27() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 27
    assert doc["emit"]["show"] is True
    assert doc["emit"]["when"] is True
    assert doc["emit"]["dynamic_list"] is True


def test_e1_emit_show_when_list_table() -> None:
    html = emit_html(FIXTURE, title="e1")
    assert 'data-role="show"' in html
    assert 'data-role="when"' in html
    assert 'data-when-branch="then"' in html
    assert 'data-when-branch="else"' in html
    assert 'data-ourui-bind="items"' in html
    assert 'data-ourui-bind="rows"' in html
    assert 'data-ourui-columns=' in html
    assert "Alpha" in html
    assert "Ada" in html


def test_e1_crud_example_compiles() -> None:
    path = ROOT / "examples" / "enterprise" / "crud_app.py"
    doc = compile_dump(path)
    assert doc["version"] == 27
    html = emit_html(path, title="crud")
    assert "Acme Admin" in html
    assert 'data-role="table"' in html
