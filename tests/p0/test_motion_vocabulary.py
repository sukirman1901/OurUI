"""ADR-012 motion vocabulary — M0 tokens + M1 patterns + aliases."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.design.motion import (
    MOTION_CATALOG_VERSION,
    catalog_summary,
    list_patterns,
    motion_css_class,
    resolve_motion,
)
from ourui.design.motion_css import motion_host_css
from ourui.pipeline import DUMP_SCHEMA_VERSION, compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "motion_vocab_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_resolve_legacy_aliases() -> None:
    assert resolve_motion("enter") == "reveal.fade-up"
    assert resolve_motion("reveal") == "reveal.mask-wipe"
    assert resolve_motion("press") == "press.scale"
    assert resolve_motion("text.word-reveal") == "text.word-reveal"
    assert resolve_motion("nope") == "none"


def test_catalog_has_stable_and_experimental() -> None:
    summary = catalog_summary()
    assert summary["version"] == MOTION_CATALOG_VERSION
    assert summary["stable_count"] == summary["total"] == 146
    assert summary["experimental_count"] == 0
    assert summary["phases"] == {"m1": 12, "m2": 17, "m3": 117}
    assert all(p.emit and p.status == "stable" for p in list_patterns())


def test_motion_css_class() -> None:
    assert motion_css_class("reveal.fade-up") == "ourui-motion-reveal-fade-up"
    assert motion_css_class("none") == ""


def test_dump_schema_30_motion() -> None:
    doc = compile_dump(FIXTURE)
    assert DUMP_SCHEMA_VERSION == 30
    assert doc["version"] == 30
    assert doc["emit"]["motion"] is True
    assert doc["motion"]["version"] == MOTION_CATALOG_VERSION
    assert doc["attestation"]["motion_catalog"] == MOTION_CATALOG_VERSION
    # legacy enter resolved in RTR
    rtr = doc["rtr"]
    motions = [
        n.get("attributes", {}).get("motion")
        for n in rtr["nodes"].values()
        if n.get("attributes", {}).get("motion")
    ]
    assert "reveal.fade-up" in motions or "hero.stagger-copy" in motions
    assert "text.word-reveal" in motions
    assert "reveal.split" in motions
    assert "enter" not in motions


def test_emit_m0_tokens_and_m1_classes() -> None:
    html_out = emit_html(FIXTURE, title="Motion")
    css = motion_host_css()
    assert "--ourui-motion-ease:" in html_out
    assert "--ourui-motion-duration:" in html_out
    assert "ourui-motion-reveal-fade-up" in html_out
    assert "ourui-motion-text-word-reveal" in html_out
    assert "ourui-motion-scroll-fade-in-view" in html_out
    assert "ourui-motion-reveal-split" in html_out
    assert "ourui-motion-text-marquee" in html_out
    assert "ourui-motion-flow-logo-marquee" in html_out
    assert 'data-ourui-motion="hero.stagger-copy"' in html_out
    assert 'data-ourui-motion="reveal.split"' in html_out
    assert "ourui-motion-scroll-counter" in css
    assert "ourui-motion-perspective-coverflow" in css
    assert "ourui-motion-hero-parallax" in css
    assert "initMotion" in html_out
    assert "prefers-reduced-motion" in html_out
