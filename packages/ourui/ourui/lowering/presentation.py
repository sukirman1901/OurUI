"""Presentation Lowering: IIR → Presentation Graph (RFC-001 Option A)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.node import LAYOUT_PASSTHROUGH

# IIR kinds that carry presentation meaning (roles / chrome / controls)
_PRESENTATION_KINDS = frozenset(
    {
        "Page",
        "Hero",
        "Section",
        "Shell",
        "Nav",
        "Footer",
        "Meta",
        "Button",
        "Text",
        "Card",
        "Grid",
        "Link",
        "Input",
        "Select",
        "Toggle",
        "Slider",
        "ThemeToggle",
        "Canvas",
        "Frame",
        "Image",
        "Icon",
        "Code",
        "CopyButton",
        "Menu",
    }
)


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
        for key in LAYOUT_PASSTHROUGH:
            if key in attrs and not isinstance(attrs[key], dict):
                if key == "layout":
                    node["shell_layout"] = attrs[key]
                elif key in {"color", "variant", "bg"}:
                    node.setdefault("tone", attrs[key])
                else:
                    node[key] = attrs[key]
        # layout attr is not in LAYOUT_PASSTHROUGH but used as shell_layout
        if "layout" in attrs and not isinstance(attrs["layout"], dict):
            node["shell_layout"] = attrs["layout"]
        pg.nodes[nid] = node
    return pg
