"""RFC-002: Resolved Design in dump (PG + theme tokens)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.design import DEFAULT_PAGE, resolve_design
from ourui.pipeline import compile_dump, compile_to_rtr
from ourui.theme import DEFAULT_LIGHT

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "example.py"
THEME = Path(__file__).parent / "fixtures" / "theme_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_includes_resolved_design() -> None:
    doc = compile_dump(FIXTURE)
    assert doc["version"] == 30
    assert "resolved_design" in doc
    assert doc["emit"]["resolved_design"] is True
    rd = doc["resolved_design"]
    assert "pack" not in rd
    assert "pack_version" not in rd
    assert rd["mode"] == "light"
    assert rd["density"] == "comfortable"
    assert rd["page"]["max_width"] == DEFAULT_PAGE["max_width"]
    assert rd["nodes"]
    assert "primary" in rd["tokens"]["light"]
    assert "pack" not in doc["attestation"]


def test_button_primary_resolves_fill_fg() -> None:
    artifacts = compile_to_rtr(FIXTURE)
    rd = artifacts["resolved_design"].to_dict()
    buttons = [n for n in rd["nodes"].values() if n.get("kind") == "Button"]
    assert buttons
    primary = [b for b in buttons if b.get("tone") == "primary"]
    assert primary
    for b in primary:
        assert b["resolved"]["fill"] == "#1a5f4a"
        assert b["resolved"]["fg"] == "#f5faf8"
        assert "resolve:design" in b["provenance"]


def test_theme_overrides_flow_into_resolved_design() -> None:
    artifacts = compile_to_rtr(THEME)
    rd = artifacts["resolved_design"].to_dict()
    button = next(n for n in rd["nodes"].values() if n.get("kind") == "Button")
    assert button["resolved"]["fill"] == "#112233"


def test_theme_defaults_seed_tokens() -> None:
    assert DEFAULT_LIGHT["primary"]
    assert DEFAULT_LIGHT["bg"] == "#fafafa"
    assert "Fraunces" not in DEFAULT_LIGHT["font_display"]


def test_resolve_design_pure_without_pipeline() -> None:
    pg = {
        "nodes": {
            "n1": {
                "id": "n1",
                "kind": "Button",
                "role": "button",
                "tone": "primary",
                "provenance": ["lowering:presentation"],
            }
        },
        "roots": ["n1"],
    }
    rd = resolve_design(pg, mode="light")
    assert rd.nodes["n1"]["resolved"]["fill"] == DEFAULT_LIGHT["primary"]


def test_untoned_button_defaults_to_primary() -> None:
    pg = {
        "nodes": {
            "n1": {
                "id": "n1",
                "kind": "Button",
                "role": "button",
                "provenance": ["lowering:presentation"],
            }
        },
        "roots": ["n1"],
    }
    rd = resolve_design(pg, mode="light")
    assert rd.nodes["n1"]["resolved"]["fill"] == DEFAULT_LIGHT["primary"]
    assert rd.nodes["n1"]["resolved"]["fg"] == DEFAULT_LIGHT["primary_fg"]
