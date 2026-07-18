"""Phase S1: ui.Link + layout intent (stack / row / split-3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.pipeline import compile_to_rtr, emit_html

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_link_emits_anchor_with_href(tmp_path: Path) -> None:
    src = tmp_path / "link_app.py"
    src.write_text(
        "from ourui import ui\n"
        'page = ui.Page(\n'
        '    ui.Hero(title="Home"),\n'
        '    ui.Link("Open Studio", href="/app"),\n'
        '    ui.Link("Docs", href="https://example.com/docs"),\n'
        ")\n",
        encoding="utf-8",
    )
    html_out = emit_html(src)
    assert '<a' in html_out
    assert 'href="/app"' in html_out
    assert "Open Studio" in html_out
    assert 'href="https://example.com/docs"' in html_out
    assert 'target="_blank"' in html_out
    assert 'rel="noopener noreferrer"' in html_out
    # Internal links must not force new tab
    assert html_out.count('target="_blank"') == 1


def test_link_role_on_rtr(tmp_path: Path) -> None:
    src = tmp_path / "link_rtr.py"
    src.write_text(
        "from ourui import ui\n"
        'page = ui.Page(ui.Link("About", href="/about", color="primary"))\n',
        encoding="utf-8",
    )
    rtr = compile_to_rtr(src)["rtr"].to_dict()
    link_nodes = [
        n for n in rtr["nodes"].values() if n.get("attributes", {}).get("role") == "link"
    ]
    assert link_nodes
    assert link_nodes[0]["attributes"].get("href") == "/about"


def test_split3_layout_emits_shell_class(tmp_path: Path) -> None:
    src = tmp_path / "shell_app.py"
    src.write_text(
        "from ourui import ui\n"
        "page = ui.Page(\n"
        '    ui.Shell(\n'
        '        ui.Section(title="Filters"),\n'
        '        ui.Section(title="Preview"),\n'
        '        ui.Section(title="Style"),\n'
        '        layout="split-3",\n'
        "    ),\n"
        '    route="/app",\n'
        ")\n",
        encoding="utf-8",
    )
    html_out = emit_html(src)
    assert "ourui-shell-split-3" in html_out
    assert "Filters" in html_out
    assert "Preview" in html_out
    assert "Style" in html_out


def test_section_layout_stack_class(tmp_path: Path) -> None:
    src = tmp_path / "stack_app.py"
    src.write_text(
        "from ourui import ui\n"
        'page = ui.Page(ui.Section(title="Nav", layout="stack", children=[ui.Text("A")]))\n',
        encoding="utf-8",
    )
    html_out = emit_html(src)
    assert "ourui-shell-stack" in html_out
