"""RFC-001: Presentation Graph in dump (Option A lowering)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, compile_to_rtr

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_includes_presentation_graph() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 15
    assert "presentation_graph" in doc
    pg = doc["presentation_graph"]
    assert "nodes" in pg and "roots" in pg
    assert pg["nodes"]
    sample = next(iter(pg["nodes"].values()))
    assert "role" in sample
    assert "lowering:presentation" in sample.get("provenance", [])


def test_presentation_graph_has_link_tone() -> None:
    # example may not have Link; compile demo if present
    demo = ROOT / "demo" / "app.py"
    if not demo.exists():
        pytest.skip("demo app missing")
    artifacts = compile_to_rtr(demo, route="/")
    pg = artifacts["presentation_graph"].to_dict()
    links = [n for n in pg["nodes"].values() if n.get("kind") == "Link"]
    assert links
    assert any(n.get("href") == "/app" for n in links)
