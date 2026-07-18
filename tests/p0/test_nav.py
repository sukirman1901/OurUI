"""Phase S3a: ui.Nav + placement + tone."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, compile_to_rtr, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "nav_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_includes_nav() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 30
    kinds = {n["kind"] for n in doc["semantic_graph"]["nodes"].values()}
    assert "Nav" in kinds
    nav = next(n for n in doc["semantic_graph"]["nodes"].values() if n["kind"] == "Nav")
    assert nav["attributes"]["placement"] == "sticky-top"
    assert nav["attributes"]["tone"] == "glass"
    assert isinstance(nav["attributes"].get("items"), list)
    assert nav["attributes"]["items"]


def test_emit_nav_html() -> None:
    html_out = emit_html(FIXTURE, title="Nav")
    assert "<nav" in html_out
    assert "ourui-nav-sticky-top" in html_out
    assert "ourui-nav-glass" in html_out
    assert "ourui-nav-brand" in html_out
    assert "ourui-nav-items" in html_out
    assert "ourui-nav-actions" in html_out
    assert 'href="/app"' in html_out


def test_rtr_nav_slots() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rtr = artifacts["rtr"].to_dict()
    nav = next(n for n in rtr["nodes"].values() if n.get("attributes", {}).get("role") == "nav")
    assert nav["attributes"]["placement"] == "sticky-top"
    assert nav["kind"] == "Container"
