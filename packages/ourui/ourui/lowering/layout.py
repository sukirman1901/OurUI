from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.node import LAYOUT_PASSTHROUGH, SHELL_LAYOUT_INTENTS, Node, SourceSpan

# IIR kind → LTR layout object kind
_LAYOUT_KIND: dict[str, str] = {
    "Page": "Column",
    "Hero": "Column",
    "Section": "Column",
    "Shell": "Row",
    "Nav": "Row",
    "Footer": "Row",
    "Meta": "Box",
    "Grid": "Grid",
    "Card": "Box",
    "Button": "Box",
    "Text": "Box",
    "Link": "Box",
    "Input": "Box",
    "Select": "Box",
    "Toggle": "Box",
    "Slider": "Box",
    "ThemeToggle": "Box",
    "Canvas": "Box",
    "Frame": "Box",
    "Image": "Box",
    "Icon": "Box",
    "Code": "Box",
    "CopyButton": "Box",
    "Menu": "Box",
    "Form": "Column",
    "Dialog": "Box",
    "Toast": "Box",
    "List": "Column",
    "Table": "Box",
    "Empty": "Box",
    "Spinner": "Box",
    "Alert": "Box",
}

_AXIS: dict[str, str] = {
    "Column": "vertical",
    "Grid": "grid",
    "Box": "none",
    "Row": "horizontal",
    "Stack": "overlay",
    "Spacer": "none",
}

_SHELL_TO_LTR: dict[str, str] = {
    "stack": "Column",
    "row": "Row",
    "split-2": "Grid",
    "split-3": "Grid",
    "split-sidebar": "Grid",
    "grid": "Grid",
}


@dataclass
class LTR:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)
    handlers: dict[str, dict[str, Any]] = field(default_factory=dict)
    states: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: node for nid, node in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
            "states": {k: self.states[k] for k in sorted(self.states)},
        }


def _span_from_dict(data: dict[str, Any]) -> SourceSpan:
    return SourceSpan(
        path=data["path"],
        start_line=data["start_line"],
        start_col=data["start_col"],
        end_line=data["end_line"],
        end_col=data["end_col"],
    )


def _resolve_layout_kind(intent_kind: str, shell_layout: str | None) -> str:
    if shell_layout in _SHELL_TO_LTR:
        return _SHELL_TO_LTR[shell_layout]
    return _LAYOUT_KIND.get(intent_kind, "Box")


def lower_to_ltr(iir: Any) -> LTR:
    """Layout Lowering: IIR → Layout Object Tree (no host/HTML semantics)."""
    ltr = LTR(roots=list(iir.roots))
    for nid, inode in iir.nodes.items():
        intent_kind = inode["kind"]
        raw_attrs = inode.get("attributes", {})
        shell_layout = raw_attrs.get("layout")
        if shell_layout is not None and shell_layout not in SHELL_LAYOUT_INTENTS:
            shell_layout = None
        layout_kind = _resolve_layout_kind(intent_kind, shell_layout if isinstance(shell_layout, str) else None)
        props: dict[str, Any] = {
            "axis": _AXIS.get(layout_kind, "none"),
            "from_intent": intent_kind,
        }
        if isinstance(shell_layout, str):
            props["shell_layout"] = shell_layout
        for key in LAYOUT_PASSTHROUGH:
            if key in raw_attrs:
                props[key] = raw_attrs[key]
        if "events" in inode:
            props["events"] = dict(inode["events"])
        if "binds" in inode:
            props["binds"] = dict(inode["binds"])

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
    ltr.handlers = dict(getattr(iir, "handlers", {}))
    ltr.states = dict(getattr(iir, "states", {}))
    return ltr
