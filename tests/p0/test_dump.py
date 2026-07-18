from __future__ import annotations

import json
from pathlib import Path

import pytest

from ourui.lowering.render import HOST_KINDS
from ourui.pipeline import compile_dump, dump_json
from ourui.serialize import dumps_deterministic

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"
GOLDEN = Path(__file__).parent / "goldens" / "example.dump.json"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_has_required_sections() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 13
    for key in (
        "semantic_graph",
        "dependency_graph",
        "iir",
        "presentation_graph",
        "resolved_design",
        "ltr",
        "rtr",
        "emit",
    ):
        assert key in doc
    assert doc["emit"]["js"] is True
    assert doc["emit"]["state"] is True
    assert doc["emit"]["components"] is True
    assert "get_started" in doc["iir"]["handlers"]
    assert doc["iir"]["handlers"]["get_started"]["kind"] == "server"
    assert "count" in doc["iir"]["states"]
    assert doc["iir"]["states"]["count"]["initial"] == 0
    assert "FeatureCard" in doc["semantic_graph"]["components"]
    assert "CounterPanel" in doc["semantic_graph"]["components"]
    assert doc["semantic_graph"]["routes"] == {"/": "n0001"}
    assert doc["rtr"]["roots"]
    assert any(e["kind"] == "uses_theme" for e in doc["dependency_graph"]["edges"])


def test_dump_deterministic() -> None:
    assert dump_json(FIXTURE) == dump_json(FIXTURE)


def test_iir_domains_present() -> None:
    doc = compile_dump(FIXTURE)
    domains = {n["domain"] for n in doc["iir"]["nodes"].values()}
    assert "intent" in domains
    assert "presentation" in domains


def test_ltr_layout_kinds() -> None:
    doc = compile_dump(FIXTURE)
    kinds = {n["kind"] for n in doc["ltr"]["nodes"].values()}
    assert "Column" in kinds
    assert "Box" in kinds
    assert "Hero" not in kinds
    for node in doc["ltr"]["nodes"].values():
        assert "lowering:layout" in node["provenance"]


def test_rtr_host_nodes() -> None:
    doc = compile_dump(FIXTURE)
    kinds = {n["kind"] for n in doc["rtr"]["nodes"].values()}
    assert kinds <= HOST_KINDS
    assert "Container" in kinds
    assert "Text" in kinds
    # No HTML tags, no layout/intent kinds as HostNode kinds
    for forbidden in ("button", "div", "Column", "Box", "Hero", "Button", "Page"):
        assert forbidden not in kinds
    for node in doc["rtr"]["nodes"].values():
        assert "lowering:render" in node["provenance"]
        assert node["metadata"].get("host") is True


def test_rtr_carries_click_events() -> None:
    doc = compile_dump(FIXTURE)
    button = next(n for n in doc["rtr"]["nodes"].values() if n["attributes"].get("role") == "button")
    assert button["attributes"]["events"]["click"] == "get_started"


def test_rtr_binds_state_text() -> None:
    doc = compile_dump(FIXTURE)
    bound = [
        n
        for n in doc["rtr"]["nodes"].values()
        if n["kind"] == "Text" and n["attributes"].get("bind") == "count"
    ]
    assert bound
    assert bound[0]["attributes"]["content"] == "0"


def test_components_expand_in_provenance() -> None:
    doc = compile_dump(FIXTURE)
    cards = [n for n in doc["semantic_graph"]["nodes"].values() if n["kind"] == "Card"]
    assert len(cards) >= 2
    assert any("expand:FeatureCard" in n["provenance"] for n in cards)
    sections = [n for n in doc["semantic_graph"]["nodes"].values() if n["kind"] == "Section"]
    assert any("expand:CounterPanel" in n["provenance"] for n in sections)


def test_golden_dump() -> None:
    GOLDEN.parent.mkdir(parents=True, exist_ok=True)
    actual = dump_json(FIXTURE)
    if not GOLDEN.exists():
        GOLDEN.write_text(actual, encoding="utf-8")
    expected_norm = dumps_deterministic(json.loads(GOLDEN.read_text(encoding="utf-8")))
    assert actual == expected_norm
