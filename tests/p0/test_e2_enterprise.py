"""E2–E5: density, check profile, attestation (no packs)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.cli import main as cli_main
from ourui.diagnostics import collect_a11y_diagnostics
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "examples" / "tutorial" / "06_counter_app.py"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_dump_schema_30_attestation() -> None:
    doc = compile_dump(SAMPLE)
    assert doc["version"] == 30
    assert doc["emit"]["density"] is True
    assert doc["emit"]["csp"] is True
    assert doc["emit"]["attestation"] is True
    assert doc["emit"]["csrf"] is True
    assert doc["emit"]["motion"] is True
    assert "packs" not in doc["emit"]
    rd = doc["resolved_design"]
    assert "pack" not in rd
    assert rd["density"] == "comfortable"
    att = doc["attestation"]
    assert att["schema"] == 30
    assert att["motion_catalog"]
    assert "pack" not in att
    assert isinstance(att.get("sha256"), str) and len(att["sha256"]) == 64


def test_density_compact_emit_class(tmp_path: Path) -> None:
    src = tmp_path / "dense.py"
    src.write_text(
        """
from ourui import ui
theme = ui.Theme(density="compact")
page = ui.Page(ui.Hero(title="Dense"), ui.Button("Ok", color="primary"))
""",
        encoding="utf-8",
    )
    doc = compile_dump(src)
    assert doc["resolved_design"]["density"] == "compact"
    html = emit_html(src, title="dense")
    assert 'class="ourui-density-compact"' in html
    assert "ourui-root ourui-density-compact" in html
    assert 'data-ourui-csp="1"' in html


def test_a11y_diagnostics_label_alt_button(tmp_path: Path) -> None:
    src = tmp_path / "a11y.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(
    ui.Input(name="email"),
    ui.Image(src="/x.png"),
    ui.Button(""),
)
""",
        encoding="utf-8",
    )
    diags = collect_a11y_diagnostics(src)
    codes = {d.code for d in diags}
    assert "A11Y001" in codes
    assert "A11Y002" in codes
    assert "A11Y003" in codes


def test_a11y_escape_budget(tmp_path: Path) -> None:
    src = tmp_path / "escape.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(
    ui.Canvas(),
    ui.Canvas(),
    ui.Frame(srcdoc="<p>a</p>"),
    ui.Frame(srcdoc="<p>b</p>"),
)
""",
        encoding="utf-8",
    )
    diags = collect_a11y_diagnostics(src)
    assert any(d.code == "ESC001" for d in diags)


def test_check_profile_a11y_exit_0(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src = tmp_path / "warn.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(ui.Input(name="x"), ui.Button("Save", color="primary"))
""",
        encoding="utf-8",
    )
    rc = cli_main(["check", str(src), "--profile", "a11y"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "A11Y001" in out
    assert "ok" in out


def test_check_strict_promotes_warnings(tmp_path: Path) -> None:
    src = tmp_path / "strict.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(ui.Input(name="x"), ui.Button("Save", color="primary"))
""",
        encoding="utf-8",
    )
    rc = cli_main(["check", str(src), "--profile", "a11y", "--strict"])
    assert rc == 1
