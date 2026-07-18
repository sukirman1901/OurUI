"""Phase S2: form controls — Input, Select, Toggle, Slider."""

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


def test_dump_includes_form_controls() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 21
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    assert {"Input", "Select", "Toggle", "Slider"} <= kinds
    pg_kinds = {n["kind"] for n in doc["presentation_graph"]["nodes"].values()}
    assert {"Input", "Select", "Toggle", "Slider"} <= pg_kinds


def test_emit_form_control_html() -> None:
    html_out = emit_html(FIXTURE, title="Form")
    assert 'data-ourui-field="email"' in html_out
    assert 'data-ourui-field="theme"' in html_out
    assert 'data-ourui-field="enabled"' in html_out
    assert 'data-ourui-field="volume"' in html_out
    assert "<select" in html_out
    assert 'type="checkbox"' in html_out
    assert 'type="range"' in html_out
    assert 'option value="light"' in html_out


def test_rtr_select_options() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rtr = artifacts["rtr"].to_dict()
    select = next(n for n in rtr["nodes"].values() if n.get("attributes", {}).get("role") == "select")
    assert select["attributes"]["options"] == ["light", "dark"]
    slider = next(n for n in rtr["nodes"].values() if n.get("attributes", {}).get("role") == "slider")
    assert slider["attributes"]["min"] == 0
    assert slider["attributes"]["max"] == 100


def test_server_accepts_form_payload() -> None:
    result = invoke_handler(
        FIXTURE,
        "save_form",
        {"email": "a@b.co", "theme": "dark", "enabled": True, "volume": "55"},
    )
    assert result["state"]["email"] == "a@b.co"
    assert result["state"]["theme"] == "dark"
    assert result["state"]["enabled"] is True
    assert result["state"]["volume"] == 55
    assert "a@b.co|dark|True|55" in str(result["result"])
