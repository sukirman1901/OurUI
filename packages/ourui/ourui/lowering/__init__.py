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

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: node for nid, node in sorted(self.nodes.items())},
            "roots": list(self.roots),
        }


def lower_to_iir(graph: SemanticGraph) -> IIR:
    iir = IIR(roots=list(graph.roots))
    for nid, node in graph.nodes.items():
        if node.kind == "ThemeToken":
            # Theme tokens remain in analysis graphs; not IIR intent nodes
            continue
        lowered = Node(
            id=node.id,
            kind=node.kind,
            span=node.span,
            attributes=dict(node.attributes),
            metadata={**node.metadata, "domain": domain_for(node.kind)},
            children=list(node.children),
            provenance=[*node.provenance, "lowering:intent"],
            revision=node.revision,
            generation=node.generation + 1,
        ).with_hash()
        payload = lowered.to_dict()
        payload["domain"] = domain_for(node.kind)
        iir.nodes[nid] = payload
    return iir
