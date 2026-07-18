from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
TUTORIAL = ROOT / "examples" / "tutorial"


@pytest.fixture(autouse=True)
def _chdir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


@pytest.mark.parametrize(
    "name",
    [
        "01_page.py",
        "02_components.py",
        "03_state_server.py",
        "04_routing.py",
        "05_theme.py",
        "06_counter_app.py",
    ],
)
def test_tutorial_example_dumps_and_emits(name: str) -> None:
    path = TUTORIAL / name
    assert path.is_file(), f"missing {path}"
    doc = compile_dump(path)
    assert doc["version"] >= 9
    html = emit_html(path)
    assert "<!DOCTYPE html>" in html
    assert "ourui-root" in html
