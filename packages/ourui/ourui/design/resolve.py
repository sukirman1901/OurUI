"""Design System resolution: Presentation Graph + pack → Resolved Design (RFC-002)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.theme import DEFAULT_DARK, DEFAULT_LIGHT

PACK_ID = "ourui-default"


def default_pack() -> dict[str, Any]:
    """Seed Design System pack from current theme tables (provisional migration)."""
    return {
        "id": PACK_ID,
        "modes": {
            "light": dict(DEFAULT_LIGHT),
            "dark": dict(DEFAULT_DARK),
        },
        "control": {
            "pad_block": "space_sm",
            "pad_inline": "space_md",
            "radius": "radius",
        },
    }


@dataclass
class ResolvedDesign:
    pack: str
    mode: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    tokens: dict[str, dict[str, str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pack": self.pack,
            "mode": self.mode,
            "nodes": {nid: self.nodes[nid] for nid in sorted(self.nodes)},
            "tokens": {
                "light": dict(self.tokens.get("light", {})),
                "dark": dict(self.tokens.get("dark", {})),
            },
        }


def _tone_pair(tone: str | None, mode_tokens: dict[str, str]) -> dict[str, str]:
    if not tone:
        return {
            "fill": mode_tokens.get("muted", ""),
            "fg": mode_tokens.get("muted_fg", ""),
        }
    fill_key = tone
    fg_key = f"{tone}_fg"
    if fill_key not in mode_tokens:
        fill_key = "primary"
        fg_key = "primary_fg"
    return {
        "fill": mode_tokens.get(fill_key, mode_tokens.get("primary", "")),
        "fg": mode_tokens.get(fg_key, mode_tokens.get("primary_fg", "")),
    }


def resolve_design(
    presentation_graph: Any,
    *,
    pack: dict[str, Any] | None = None,
    mode: str = "light",
    token_overrides: dict[str, dict[str, str]] | None = None,
) -> ResolvedDesign:
    """Pure resolution: PG + Design System pack → Resolved Design (no CSS)."""
    pack = pack or default_pack()
    modes = {
        "light": dict(pack.get("modes", {}).get("light", DEFAULT_LIGHT)),
        "dark": dict(pack.get("modes", {}).get("dark", DEFAULT_DARK)),
    }
    if token_overrides:
        for m in ("light", "dark"):
            if m in token_overrides:
                modes[m].update(token_overrides[m])

    mode_key = mode if mode in modes else "light"
    mode_tokens = modes[mode_key]
    control = pack.get("control") or {}
    pad_block = mode_tokens.get(control.get("pad_block", "space_sm"), mode_tokens.get("space_sm", ""))
    pad_inline = mode_tokens.get(control.get("pad_inline", "space_md"), mode_tokens.get("space_md", ""))
    radius = mode_tokens.get(control.get("radius", "radius"), mode_tokens.get("radius", ""))

    pg = presentation_graph.to_dict() if hasattr(presentation_graph, "to_dict") else dict(presentation_graph)
    nodes_in = pg.get("nodes") or {}

    out = ResolvedDesign(pack=str(pack.get("id", PACK_ID)), mode=mode_key, tokens=modes)
    for nid, node in nodes_in.items():
        tone = node.get("tone")
        if isinstance(tone, str):
            pair = _tone_pair(tone, mode_tokens)
        else:
            pair = _tone_pair(None, mode_tokens)
        resolved: dict[str, Any] = {
            "fill": pair["fill"],
            "fg": pair["fg"],
            "radius": radius,
            "pad_block": pad_block,
            "pad_inline": pad_inline,
        }
        entry = {
            "id": nid,
            "kind": node.get("kind"),
            "role": node.get("role"),
            "resolved": resolved,
            "provenance": [*node.get("provenance", []), "resolve:design"],
        }
        if tone is not None:
            entry["tone"] = tone
        if "href" in node:
            entry["href"] = node["href"]
        if "shell_layout" in node:
            entry["shell_layout"] = node["shell_layout"]
        out.nodes[nid] = entry
    return out
