"""Structured compile diagnostics (Phase V) + enterprise a11y profile (E2)."""

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


_FORM_KINDS = frozenset({"Input", "Select", "Toggle", "Slider"})
_ESCAPE_KINDS = frozenset({"Canvas", "Frame"})
_ESCAPE_BUDGET = 3


def _span_fields(node: Any, fallback_path: str) -> dict[str, Any]:
    span = getattr(node, "span", None)
    if span is None:
        return {
            "path": fallback_path,
            "start_line": 1,
            "end_line": 1,
            "start_col": 0,
            "end_col": 0,
        }
    data = span.to_dict() if hasattr(span, "to_dict") else dict(span)
    return {
        "path": str(data.get("path", fallback_path)),
        "start_line": int(data.get("start_line", 1)),
        "end_line": int(data.get("end_line", 1)),
        "start_col": int(data.get("start_col", 0)),
        "end_col": int(data.get("end_col", 0)),
    }


def collect_enterprise_diagnostics(path: str | Path) -> list[Diagnostic]:
    """Enterprise a11y / escape-budget warnings (profile ``enterprise``)."""
    from ourui.analysis import build_semantic_graph

    path = Path(path)
    display = path.as_posix()
    out: list[Diagnostic] = []
    try:
        sg, _dg = build_semantic_graph(path)
    except Exception as exc:  # noqa: BLE001
        out.append(
            Diagnostic(
                code="E999",
                message=str(exc),
                path=display,
            )
        )
        return out

    escape_count = 0
    for node in sg.nodes.values():
        kind = node.kind
        attrs = node.attributes or {}
        span = _span_fields(node, display)

        if kind in _FORM_KINDS:
            label = attrs.get("label")
            has_label = isinstance(label, str) and label.strip() != ""
            if not has_label:
                name = attrs.get("name")
                hint = f" (name={name!r})" if isinstance(name, str) and name else ""
                out.append(
                    Diagnostic(
                        code="A11Y001",
                        message=f"{kind} without label={hint}",
                        severity="warning",
                        **span,
                    )
                )

        if kind == "Image" and "alt" not in attrs:
            out.append(
                Diagnostic(
                    code="A11Y002",
                    message="Image without alt= (empty alt is OK for decorative images)",
                    severity="warning",
                    **span,
                )
            )

        if kind == "Button":
            text = attrs.get("text")
            accessible = False
            if isinstance(text, str) and text.strip():
                accessible = True
            elif isinstance(text, dict) and ("__state__" in text or text):
                accessible = True
            elif node.children:
                accessible = True
            aria = attrs.get("aria_label") or attrs.get("aria-label")
            if isinstance(aria, str) and aria.strip():
                accessible = True
            if not accessible:
                out.append(
                    Diagnostic(
                        code="A11Y003",
                        message="Button without accessible text",
                        severity="warning",
                        **span,
                    )
                )

        if kind in _ESCAPE_KINDS:
            escape_count += 1

        if kind == "Frame":
            has_srcdoc = "srcdoc" in attrs
            bind = attrs.get("bind")
            if has_srcdoc or bind is not None:
                out.append(
                    Diagnostic(
                        code="SEC001",
                        message=(
                            "Frame with srcdoc/bind is an HTML escape hatch; "
                            "sandbox and sanitize untrusted content at the app layer"
                        ),
                        severity="warning",
                        **span,
                    )
                )

    if escape_count > _ESCAPE_BUDGET:
        out.append(
            Diagnostic(
                code="ESC001",
                message=(
                    f"Escape budget exceeded: {escape_count} Canvas/Frame nodes "
                    f"(budget {_ESCAPE_BUDGET})"
                ),
                path=display,
                severity="warning",
            )
        )

    return out
