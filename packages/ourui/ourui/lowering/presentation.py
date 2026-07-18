"""Presentation Lowering: IIR → Presentation Graph (RFC-001 Option A)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# IIR kinds that carry presentation meaning (roles / chrome / controls)
_PRESENTATION_KINDS = frozenset(
    {
        "Page",
        "Hero",
        "Section",
        "Shell",
        "Button",
        "Text",
        "Card",
        "Grid",
        "Link",
    }
)

_PASSTHROUGH = ("color", "variant", "bg", "href", "external", "layout", "text", "title")


@dataclass
class PresentationGraph:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: self.nodes[nid] for nid in sorted(self.nodes)},
            "roots": list(self.roots),
        }


def lower_to_presentation_graph(iir: Any) -> PresentationGraph:
    """Derive a host-neutral Presentation Graph from IIR (no tokens, no CSS)."""
    pg = PresentationGraph(roots=list(iir.roots))
    for nid, inode in iir.nodes.items():
        kind = inode.get("kind", "")
        if kind not in _PRESENTATION_KINDS:
            continue
        attrs = inode.get("attributes", {}) or {}
        node: dict[str, Any] = {
            "id": nid,
            "kind": kind,
            "role": kind.lower(),
            "children": list(inode.get("children", [])),
            "provenance": [*inode.get("provenance", []), "lowering:presentation"],
        }
        for key in _PASSTHROUGH:
            if key in attrs and not isinstance(attrs[key], dict):
                # `layout` on Shell/Section is shell_layout intent in presentation
                if key == "layout":
                    node["shell_layout"] = attrs[key]
                elif key in {"color", "variant", "bg"}:
                    node.setdefault("tone", attrs[key])
                else:
                    node[key] = attrs[key]
        pg.nodes[nid] = node
    return pg
