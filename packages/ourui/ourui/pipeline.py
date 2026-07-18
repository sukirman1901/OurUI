from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ourui.analysis import build_semantic_graph
from ourui.design import PACK_ID, PACK_VERSION, resolve_design
from ourui.emit import emit_bundle, emit_html_document
from ourui.lowering import lower_to_iir, lower_to_ltr, lower_to_presentation_graph, lower_to_rtr
from ourui.serialize import dumps_deterministic

DUMP_SCHEMA_VERSION = 29


def _display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def compile_to_rtr(path: str | Path, *, route: str | None = None) -> dict[str, Any]:
    path = Path(path)
    sg, dg = build_semantic_graph(path)
    if route is not None:
        root_id = sg.routes.get(route)
        if root_id is None:
            raise KeyError(f"Unknown route: {route!r}")
        sg.roots = [root_id]
    elif sg.routes:
        default_route = "/" if "/" in sg.routes else sorted(sg.routes)[0]
        sg.roots = [sg.routes[default_route]]
    iir = lower_to_iir(sg)
    presentation_graph = lower_to_presentation_graph(iir)
    resolved_design = resolve_design(
        presentation_graph,
        token_overrides=sg.tokens,
        density=getattr(sg, "density", None),
        pack_id=getattr(sg, "pack", None),
        recipe_id=getattr(sg, "recipe", None),
    )
    ltr = lower_to_ltr(iir)
    rtr = lower_to_rtr(ltr)
    return {
        "source": _display_path(path),
        "semantic_graph": sg,
        "dependency_graph": dg,
        "iir": iir,
        "presentation_graph": presentation_graph,
        "resolved_design": resolved_design,
        "ltr": ltr,
        "rtr": rtr,
    }


def compile_dump(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    artifacts = compile_to_rtr(path)
    sg = artifacts["semantic_graph"].to_dict()
    rd = artifacts["resolved_design"]
    rd_dict = rd.to_dict() if hasattr(rd, "to_dict") else dict(rd)
    dump: dict[str, Any] = {
        "version": DUMP_SCHEMA_VERSION,
        "source": artifacts["source"],
        "semantic_graph": sg,
        "dependency_graph": artifacts["dependency_graph"].to_dict(),
        "iir": artifacts["iir"].to_dict(),
        "presentation_graph": artifacts["presentation_graph"].to_dict(),
        "resolved_design": rd_dict,
        "ltr": artifacts["ltr"].to_dict(),
        "rtr": artifacts["rtr"].to_dict(),
        "derived": sg.get("derived", {}),
        "diagnostics": sg.get("diagnostics", []),
        "attestation": {
            "schema": DUMP_SCHEMA_VERSION,
            "pack": str(rd_dict.get("pack", PACK_ID)),
            "pack_version": str(rd_dict.get("pack_version", PACK_VERSION)),
        },
        "emit": {
            "html": True,
            "css": True,
            "js": True,
            "state": True,
            "components": True,
            "tokens": True,
            "presentation_graph": True,
            "resolved_design": True,
            "host_contract": True,
            "host_contract_primary": True,
            "diagnostics": True,
            "derived": True,
            "form": True,
            "dialog": True,
            "toast": True,
            "list": True,
            "table": True,
            "show": True,
            "when": True,
            "dynamic_list": True,
            "density": True,
            "csp": True,
            "attestation": True,
            "csrf": True,
            "security_headers": True,
            "packs": True,
            "recipes": True,
        },
    }
    digest_body = dumps_deterministic(dump)
    dump["attestation"]["sha256"] = hashlib.sha256(digest_body.encode("utf-8")).hexdigest()
    return dump


def dump_json(path: str | Path) -> str:
    return dumps_deterministic(compile_dump(path))


def emit_html(
    path: str | Path,
    *,
    title: str | None = None,
    route: str | None = None,
    state_values: dict[str, Any] | None = None,
    hmr: bool = False,
    csrf_token: str | None = None,
    csp_nonce: str | None = None,
) -> str:
    """Compile source → RTR + Resolved Design → HTML (Host Contract)."""
    artifacts = compile_to_rtr(path, route=route)
    doc_title = title or Path(path).stem
    return emit_html_document(
        artifacts["rtr"].to_dict(),
        title=doc_title,
        state_values=state_values,
        hmr=hmr,
        resolved_design=artifacts["resolved_design"],
        csrf_token=csrf_token,
        csp_nonce=csp_nonce,
    )


def emit_all(path: str | Path, *, title: str | None = None) -> dict[str, str]:
    artifacts = compile_to_rtr(path)
    doc_title = title or Path(path).stem
    return emit_bundle(
        artifacts["rtr"].to_dict(),
        title=doc_title,
        resolved_design=artifacts["resolved_design"],
    )
