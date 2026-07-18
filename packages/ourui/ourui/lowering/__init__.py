from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.analysis import SemanticGraph
from ourui.lowering.layout import LTR, lower_to_ltr
from ourui.lowering.render import RTR, lower_to_rtr
from ourui.node import INTENT_KINDS, PRESENTATION_KINDS, Node

__all__ = [
    "IIR",
    "LTR",
    "RTR",
    "domain_for",
    "lower_to_iir",
    "lower_to_ltr",
    "lower_to_rtr",
]


def domain_for(kind: str) -> str:
    if kind in INTENT_KINDS:
        return "intent"
    if kind in PRESENTATION_KINDS:
        return "presentation"
    if kind == "ThemeToken":
        return "presentation"
    return "behavior"


@dataclass
class IIR:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)
    handlers: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: node for nid, node in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
        }


def lower_to_iir(graph: SemanticGraph) -> IIR:
    iir = IIR(roots=list(graph.roots), handlers=dict(graph.handlers))
    for nid, node in graph.nodes.items():
        if node.kind == "ThemeToken":
            continue
        attrs = dict(node.attributes)
        events: dict[str, str] = {}
        on_click = attrs.pop("on_click", None)
        if isinstance(on_click, dict) and "__handler__" in on_click:
            events["click"] = str(on_click["__handler__"])

        lowered = Node(
            id=node.id,
            kind=node.kind,
            span=node.span,
            attributes=attrs,
            metadata={
                **node.metadata,
                "domain": domain_for(node.kind),
                **({"behavior": True} if events else {}),
            },
            children=list(node.children),
            provenance=[*node.provenance, "lowering:intent"],
            revision=node.revision,
            generation=node.generation + 1,
        ).with_hash()
        payload = lowered.to_dict()
        payload["domain"] = domain_for(node.kind)
        if events:
            payload["events"] = events
            payload["domain"] = "behavior" if node.kind == "Button" else payload["domain"]
            # Keep presentation kind but mark behavior events (Button stays presentation+events)
            if node.kind in PRESENTATION_KINDS:
                payload["domain"] = "presentation"
        iir.nodes[nid] = payload
    return iir
