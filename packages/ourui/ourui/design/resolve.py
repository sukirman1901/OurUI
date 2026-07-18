"""Design System resolution: Presentation Graph + pack → Resolved Design (RFC-002)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.theme import DEFAULT_DARK, DEFAULT_LIGHT

PACK_ID = "ourui-default"


PACK_VERSION = "1.0.0"

DENSITY_COMPACT: dict[str, str] = {
    "space_sm": "0.375rem",
    "space_md": "0.5rem",
    "space_lg": "0.75rem",
}


def default_pack() -> dict[str, Any]:
    """Seed Design System pack from current theme tables (provisional migration)."""
    return {
        "id": PACK_ID,
        "version": PACK_VERSION,
        "modes": {
            "light": dict(DEFAULT_LIGHT),
            "dark": dict(DEFAULT_DARK),
        },
        "control": {
            "pad_block": "space_sm",
            "pad_inline": "space_md",
            "radius": "radius",
        },
        # Page chrome recipes — host maps via tokens in _BASE_CSS.
        "page": {
            "max_width": "42rem",
            "pad_block": "space_xl",
            "pad_inline": "space_lg",
            "gap": "space_lg",
        },
        "density": {
            "default": "comfortable",
            "compact": dict(DENSITY_COMPACT),
        },
    }


@dataclass
class ResolvedDesign:
    pack: str
    mode: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    tokens: dict[str, dict[str, str]] = field(default_factory=dict)
    pack_version: str = PACK_VERSION
    density: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "pack": self.pack,
            "pack_version": self.pack_version,
            "mode": self.mode,
            "nodes": {nid: self.nodes[nid] for nid in sorted(self.nodes)},
            "tokens": {
                "light": dict(self.tokens.get("light", {})),
                "dark": dict(self.tokens.get("dark", {})),
            },
        }
        if self.density is not None:
            out["density"] = self.density
        return out


def _tone_pair(
    tone: str | None,
    mode_tokens: dict[str, str],
    *,
    fallback: str = "muted",
) -> dict[str, str]:
    """Resolve fill/fg. Untoned buttons use primary (not muted gray chips)."""
    effective = tone if tone else fallback
    fill_key = effective
    fg_key = f"{effective}_fg"
    if fill_key not in mode_tokens:
        fill_key = "primary"
        fg_key = "primary_fg"
    return {
        "fill": mode_tokens.get(fill_key, mode_tokens.get("primary", "")),
        "fg": mode_tokens.get(fg_key, mode_tokens.get("primary_fg", "")),
    }


def _fallback_tone(role: str | None) -> str:
    if role == "button":
        return "primary"
    if role == "link":
        return "primary"
    return "muted"


def resolve_design(
    presentation_graph: Any,
    *,
    pack: dict[str, Any] | None = None,
    mode: str = "light",
    token_overrides: dict[str, dict[str, str]] | None = None,
    density: str | None = None,
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

    density_meta = pack.get("density") or {}
    density_default = str(density_meta.get("default") or "comfortable")
    density_key = density if density in ("compact", "comfortable") else density_default

    pg = presentation_graph.to_dict() if hasattr(presentation_graph, "to_dict") else dict(presentation_graph)
    nodes_in = pg.get("nodes") or {}

    out = ResolvedDesign(
        pack=str(pack.get("id", PACK_ID)),
        mode=mode_key,
        tokens=modes,
        pack_version=str(pack.get("version", PACK_VERSION)),
        density=density_key,
    )
    for nid, node in nodes_in.items():
        tone = node.get("tone")
        role = node.get("role")
        if isinstance(tone, str):
            pair = _tone_pair(tone, mode_tokens)
        else:
            pair = _tone_pair(None, mode_tokens, fallback=_fallback_tone(role if isinstance(role, str) else None))
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
