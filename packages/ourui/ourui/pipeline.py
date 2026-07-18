from __future__ import annotations

from pathlib import Path
from typing import Any

from ourui.analysis import build_semantic_graph
from ourui.emit import emit_bundle, emit_html_document
from ourui.lowering import lower_to_iir, lower_to_ltr, lower_to_rtr
from ourui.serialize import dumps_deterministic


def _display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def compile_to_rtr(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    sg, dg = build_semantic_graph(path)
    iir = lower_to_iir(sg)
    ltr = lower_to_ltr(iir)
    rtr = lower_to_rtr(ltr)
    return {
        "source": _display_path(path),
        "semantic_graph": sg,
        "dependency_graph": dg,
        "iir": iir,
        "ltr": ltr,
        "rtr": rtr,
    }


def compile_dump(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    artifacts = compile_to_rtr(path)
    return {
        "version": 4,
        "source": artifacts["source"],
        "semantic_graph": artifacts["semantic_graph"].to_dict(),
        "dependency_graph": artifacts["dependency_graph"].to_dict(),
        "iir": artifacts["iir"].to_dict(),
        "ltr": artifacts["ltr"].to_dict(),
        "rtr": artifacts["rtr"].to_dict(),
        "emit": {
            "html": True,
            "css": True,
            "js": False,
        },
    }


def dump_json(path: str | Path) -> str:
    return dumps_deterministic(compile_dump(path))


def emit_html(path: str | Path, *, title: str | None = None) -> str:
    """Compile source → RTR → HTML. Emitter consumes HostNode only."""
    artifacts = compile_to_rtr(path)
    doc_title = title or Path(path).stem
    return emit_html_document(artifacts["rtr"].to_dict(), title=doc_title)


def emit_all(path: str | Path, *, title: str | None = None) -> dict[str, str]:
    artifacts = compile_to_rtr(path)
    doc_title = title or Path(path).stem
    return emit_bundle(artifacts["rtr"].to_dict(), title=doc_title)
