"""Theme(css=) — author CSS inject without editing the package."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def _emit(tmp_path: Path, source: str) -> str:
    src = tmp_path / "app.py"
    src.write_text(source, encoding="utf-8")
    return emit_html(src, title="theme-css")


def test_theme_css_appended_after_utilities(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui

CUSTOM = \"\"\"
.hero-glow {
  box-shadow: 0 0 40px color-mix(in srgb, var(--ourui-accent) 35%, transparent);
}
\"\"\"

theme = ui.Theme(primary="#18181b", css=CUSTOM)
page = ui.Page(ui.Text("Hi"))
""",
    )
    assert "/* OurUI author CSS (Theme css=) */" in html
    assert ".hero-glow {" in html
    assert "var(--ourui-accent)" in html
    # Author block comes after generated utilities
    assert html.index(".ourui-w-lg {") < html.index("/* OurUI author CSS (Theme css=) */")


def test_theme_css_inline_string(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
theme = ui.Theme(css=".x { color: var(--ourui-fg); }")
page = ui.Page(ui.Text("Hi"))
""",
    )
    assert ".x { color: var(--ourui-fg); }" in html


def test_theme_css_sanitizes_style_breakout(tmp_path: Path) -> None:
    html = _emit(
        tmp_path,
        """
from ourui import ui
theme = ui.Theme(css="x { color: red; } </style><script>alert(1)</script>")
page = ui.Page(ui.Text("Hi"))
""",
    )
    assert "</style><script>" not in html
    assert "<\\/style" in html


def test_dump_includes_author_css(tmp_path: Path) -> None:
    src = tmp_path / "app.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(css=".y { opacity: 0.5; }")
page = ui.Page(ui.Text("Hi"))
""",
        encoding="utf-8",
    )
    dump = compile_dump(src)
    assert dump["semantic_graph"].get("author_css") == ".y { opacity: 0.5; }"
    assert dump["resolved_design"].get("author_css") == ".y { opacity: 0.5; }"
