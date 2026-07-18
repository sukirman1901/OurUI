"""Enterprise E2–E5: pack version, density, check profile, attestation, kit."""

from __future__ import annotations

from pathlib import Path

import pytest

from ourui.cli import main as cli_main
from ourui.design import PACK_VERSION, default_pack
from ourui.diagnostics import collect_enterprise_diagnostics
from ourui.pipeline import compile_dump, emit_html

ROOT = Path(__file__).resolve().parents[2]
ENTERPRISE = ROOT / "examples" / "enterprise"
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def _chdir_repo(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def test_default_pack_version_and_density() -> None:
    pack = default_pack()
    assert pack["version"] == "1.2.0"
    assert pack["version"] == PACK_VERSION
    assert pack["density"]["default"] == "comfortable"
    assert "space_sm" in pack["density"]["compact"]


def test_dump_schema_30_attestation_and_pack_version() -> None:
    doc = compile_dump(ENTERPRISE / "crud_app.py")
    assert doc["version"] == 30
    assert doc["emit"]["density"] is True
    assert doc["emit"]["csp"] is True
    assert doc["emit"]["attestation"] is True
    assert doc["emit"]["csrf"] is True
    assert doc["emit"]["motion"] is True
    rd = doc["resolved_design"]
    assert rd["pack"] == "ourui-default"
    assert rd["pack_version"] == "1.2.0"
    assert rd["density"] == "comfortable"
    att = doc["attestation"]
    assert att["schema"] == 30
    assert att["pack"] == "ourui-default"
    assert att["pack_version"] == "1.2.0"
    assert att["motion_catalog"]
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


def test_enterprise_diagnostics_label_alt_button(tmp_path: Path) -> None:
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
    diags = collect_enterprise_diagnostics(src)
    codes = {d.code for d in diags}
    assert "A11Y001" in codes
    assert "A11Y002" in codes
    assert "A11Y003" in codes


def test_enterprise_escape_budget(tmp_path: Path) -> None:
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
    diags = collect_enterprise_diagnostics(src)
    assert any(d.code == "ESC001" for d in diags)


def test_check_profile_enterprise_exit_0(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src = tmp_path / "warn.py"
    src.write_text(
        """
from ourui import ui
page = ui.Page(ui.Input(name="x"), ui.Button("Save", color="primary"))
""",
        encoding="utf-8",
    )
    rc = cli_main(["check", str(src), "--profile", "enterprise"])
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
    rc = cli_main(["check", str(src), "--profile", "enterprise", "--strict"])
    assert rc == 1


@pytest.mark.parametrize(
    "name",
    ["crud_app.py", "settings_app.py", "audit_app.py", "ai_console_app.py"],
)
def test_enterprise_kit_apps_schema_29(name: str) -> None:
    path = ENTERPRISE / name
    doc = compile_dump(path)
    assert doc["version"] == 30
    html = emit_html(path, title=path.stem)
    assert "Acme" in html or "acme" in html.lower() or path.stem.replace("_", " ") in html.lower()
