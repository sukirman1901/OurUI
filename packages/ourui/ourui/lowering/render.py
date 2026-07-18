from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.node import Node, SourceSpan

# LTR layout kind → HostNode kind
_HOST_KIND: dict[str, str] = {
    "Column": "Container",
    "Row": "Container",
    "Grid": "Container",
    "Stack": "Container",
    "Box": "Leaf",
    "Spacer": "Leaf",
}

HOST_KINDS = frozenset({"Container", "Leaf", "Text", "Drawing", "Slot"})


@dataclass
class RTR:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)
    handlers: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: node for nid, node in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
        }


def _span_from_dict(data: dict[str, Any]) -> SourceSpan:
    return SourceSpan(
        path=data["path"],
        start_line=data["start_line"],
        start_col=data["start_col"],
        end_line=data["end_line"],
        end_col=data["end_col"],
    )


def _next_text_id(counter: list[int]) -> str:
    counter[0] += 1
    return f"text{counter[0]:04d}"


def lower_to_rtr(ltr: Any) -> RTR:
    """Render Lowering: LTR → host-independent Render Tree (HostNode only)."""
    rtr = RTR(roots=list(ltr.roots))
    text_counter = [0]
    # First pass: main host nodes
    for nid, lnode in ltr.nodes.items():
        layout_kind = lnode["kind"]
        host_kind = _HOST_KIND.get(layout_kind, "Leaf")
        attrs = lnode.get("attributes", {})
        from_intent = attrs.get("from_intent", layout_kind)
        props: dict[str, Any] = {
            "layout": attrs.get("axis", "none"),
            "role": _role_for(from_intent),
            "from_layout": layout_kind,
            "from_intent": from_intent,
        }
        if "events" in attrs:
            props["events"] = dict(attrs["events"])
        children = list(lnode.get("children", []))

        # Promote textual props to Text HostNodes (still no HTML)
        text_children: list[str] = []
        for prop_key in ("title", "subtitle", "text"):
            if prop_key in attrs and isinstance(attrs[prop_key], str):
                tid = _next_text_id(text_counter)
                text_node = Node(
                    id=tid,
                    kind="Text",
                    span=_span_from_dict(lnode["span"]),
                    attributes={"content": attrs[prop_key], "slot": prop_key},
                    metadata={"stage": "rtr", "host": True},
                    children=[],
                    provenance=[*lnode.get("provenance", []), "lowering:render", "expand:text"],
                    revision=lnode.get("revision", 0),
                    generation=lnode.get("generation", 0) + 1,
                ).with_hash()
                rtr.nodes[tid] = text_node.to_dict()
                text_children.append(tid)

        # Text nodes first (label), then structural children
        all_children = text_children + children

        # Box with children becomes Container so structure stays valid
        if host_kind == "Leaf" and all_children:
            host_kind = "Container"

        node = Node(
            id=nid,
            kind=host_kind,
            span=_span_from_dict(lnode["span"]),
            attributes=props,
            metadata={"stage": "rtr", "host": True},
            children=all_children,
            provenance=[*lnode.get("provenance", []), "lowering:render"],
            revision=lnode.get("revision", 0),
            generation=lnode.get("generation", 0) + 1,
        ).with_hash()
        rtr.nodes[nid] = node.to_dict()

    rtr.handlers = dict(getattr(ltr, "handlers", {}))
    return rtr


def _role_for(from_intent: str) -> str:
    """Semantic role for emitters — not an HTML tag name."""
    mapping = {
        "Page": "page",
        "Hero": "hero",
        "Section": "section",
        "Button": "button",
        "Card": "card",
        "Text": "text",
        "Grid": "grid",
    }
    return mapping.get(from_intent, from_intent.lower())
