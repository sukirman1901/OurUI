from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.node import Node, SourceSpan

# IIR kind → LTR layout object kind
_LAYOUT_KIND: dict[str, str] = {
    "Page": "Column",
    "Hero": "Column",
    "Section": "Column",
    "Grid": "Grid",
    "Card": "Box",
    "Button": "Box",
    "Text": "Box",
}

_AXIS: dict[str, str] = {
    "Column": "vertical",
    "Grid": "grid",
    "Box": "none",
    "Row": "horizontal",
    "Stack": "overlay",
    "Spacer": "none",
}


@dataclass
class LTR:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: node for nid, node in sorted(self.nodes.items())},
            "roots": list(self.roots),
        }


def _span_from_dict(data: dict[str, Any]) -> SourceSpan:
    return SourceSpan(
        path=data["path"],
        start_line=data["start_line"],
        start_col=data["start_col"],
        end_line=data["end_line"],
        end_col=data["end_col"],
    )


def lower_to_ltr(iir: Any) -> LTR:
    """Layout Lowering: IIR → Layout Object Tree (no host/HTML semantics)."""
    ltr = LTR(roots=list(iir.roots))
    for nid, inode in iir.nodes.items():
        intent_kind = inode["kind"]
        layout_kind = _LAYOUT_KIND.get(intent_kind, "Box")
        props = {
            "axis": _AXIS.get(layout_kind, "none"),
            "from_intent": intent_kind,
        }
        for key in ("title", "subtitle", "text", "variant", "color"):
            if key in inode.get("attributes", {}):
                props[key] = inode["attributes"][key]

        children = list(inode.get("children", []))

        node = Node(
            id=nid,
            kind=layout_kind,
            span=_span_from_dict(inode["span"]),
            attributes=props,
            metadata={"stage": "ltr"},
            children=children,
            provenance=[*inode.get("provenance", []), "lowering:layout"],
            revision=inode.get("revision", 0),
            generation=inode.get("generation", 0) + 1,
        ).with_hash()
        ltr.nodes[nid] = node.to_dict()
    return ltr
