"""Structured compile diagnostics (Phase V)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class Diagnostic:
    code: str
    message: str
    path: str
    start_line: int = 1
    end_line: int = 1
    start_col: int = 0
    end_col: int = 0
    severity: str = "error"  # error | warning | info

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def format_line(self) -> str:
        loc = f"{self.path}:{self.start_line}:{self.start_col}"
        return f"{self.severity}:{self.code}: {loc}: {self.message}"


def collect_diagnostics(path: str | Path) -> list[Diagnostic]:
    """Run analyze/compile and return diagnostics (including caught errors)."""
    from ourui.analysis import build_semantic_graph
    from ourui.pipeline import compile_dump

    path = Path(path)
    out: list[Diagnostic] = []
    try:
        sg, _dg = build_semantic_graph(path)
        for raw in sg.diagnostics:
            out.append(
                Diagnostic(
                    code=str(raw.get("code", "E000")),
                    message=str(raw.get("message", "")),
                    path=str(raw.get("path", path.as_posix())),
                    start_line=int(raw.get("start_line", 1)),
                    end_line=int(raw.get("end_line", 1)),
                    start_col=int(raw.get("start_col", 0)),
                    end_col=int(raw.get("end_col", 0)),
                )
            )
        compile_dump(path)
    except Exception as exc:  # noqa: BLE001
        out.append(
            Diagnostic(
                code="E999",
                message=str(exc),
                path=path.as_posix(),
            )
        )
    return out
