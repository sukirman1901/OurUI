"""Phase S2: ui.Input + form fields → @server payload."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, compile_to_rtr, emit_html
from ourui.runtime.invoke import invoke_handler

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "form_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_includes_input() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 13
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    assert "Input" in kinds
    pg = doc["presentation_graph"]
    inputs = [n for n in pg["nodes"].values() if n.get("kind") == "Input"]
    assert inputs
    assert inputs[0].get("role") == "input"
    assert inputs[0].get("name") == "email"


def test_emit_input_html() -> None:
    html_out = emit_html(FIXTURE, title="Form")
    assert 'data-ourui-field="email"' in html_out
    assert 'type="email"' in html_out
    assert 'placeholder="you@example.com"' in html_out
    assert "ourui-input" in html_out
    assert "collectFields" in html_out


def test_rtr_input_attrs() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rtr = artifacts["rtr"].to_dict()
    leaf = next(
        n
        for n in rtr["nodes"].values()
        if n.get("attributes", {}).get("role") == "input"
    )
    attrs = leaf["attributes"]
    assert attrs["name"] == "email"
    assert attrs["type"] == "email"
    assert attrs.get("bind") == "email"


def test_server_accepts_form_payload() -> None:
    result = invoke_handler(FIXTURE, "save_email", {"email": "a@b.co"})
    assert result["state"]["email"] == "a@b.co"
    assert result["state"]["saved"] == "a@b.co"
    assert result["result"] == "a@b.co"
