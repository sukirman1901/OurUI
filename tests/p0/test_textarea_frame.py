"""Textarea Input + Frame preview escape."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "textarea_frame_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_textarea_and_frame_emit() -> None:
    html = emit_html(FIXTURE, title="tf")
    assert "<textarea" in html
    assert 'data-ourui-field="source"' in html
    assert "<iframe" in html
    assert "sandbox=" in html
    assert "srcdoc=" in html
    assert 'data-ourui-bind="preview"' in html
    assert "el.srcdoc" in html  # applyState


def test_textarea_frame_in_dump() -> None:
    doc = compile_dump(FIXTURE)
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    assert "Input" in kinds
    assert "Frame" in kinds
    assert doc["version"] == 27
