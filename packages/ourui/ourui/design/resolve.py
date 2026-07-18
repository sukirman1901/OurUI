"""Presentation Graph + theme tokens → Resolved Design (RFC-002).

No named packs/recipes — seed from ``ourui.theme`` defaults + Theme overrides.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ourui.theme import DEFAULT_DARK, DEFAULT_LIGHT, default_tokens

# Page measure defaults (override via ui.Theme(page={...}))
DEFAULT_PAGE: dict[str, str] = {
    "max_width": "42rem",
    "pad_block": "space_xl",
    "pad_inline": "space_lg",
    "gap": "space_lg",
}

DENSITY_COMPACT: dict[str, str] = {
    "space_sm": "0.375rem",
    "space_md": "0.5rem",
    "space_lg": "0.75rem",
}


@dataclass
class ResolvedDesign:
    mode: str
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    tokens: dict[str, dict[str, str]] = field(default_factory=dict)
    density: str | None = None
    page: dict[str, str] = field(default_factory=dict)
    scales: dict[str, dict[str, str]] = field(default_factory=dict)
    author_css: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "mode": self.mode,
            "nodes": {nid: self.nodes[nid] for nid in sorted(self.nodes)},
            "tokens": {
                "light": dict(self.tokens.get("light", {})),
                "dark": dict(self.tokens.get("dark", {})),
            },
        }
        if self.density is not None:
            out["density"] = self.density
        if self.page:
            out["page"] = dict(self.page)
        if self.scales:
            out["scales"] = {k: dict(v) for k, v in self.scales.items()}
        if self.author_css:
            out["author_css"] = self.author_css
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
    mode: str = "light",
    token_overrides: dict[str, dict[str, str]] | None = None,
    density: str | None = None,
    scale_overrides: dict[str, dict[str, str]] | None = None,
    page_overrides: dict[str, str] | None = None,
    author_css: str | None = None,
) -> ResolvedDesign:
    """Pure resolution: PG + theme tokens → Resolved Design (no CSS)."""
    modes = default_tokens()
    if token_overrides:
        for m in ("light", "dark"):
            if m in token_overrides:
                modes[m].update(token_overrides[m])

    mode_key = mode if mode in modes else "light"
    mode_tokens = modes[mode_key]
    pad_block = mode_tokens.get("space_sm", "")
    pad_inline = mode_tokens.get("space_md", "")
    radius = mode_tokens.get("radius", "")

    density_key = density if density in ("compact", "comfortable") else "comfortable"

    page = dict(DEFAULT_PAGE)
    if page_overrides:
        page.update({str(k): str(v) for k, v in page_overrides.items()})

    scales: dict[str, dict[str, str]] = {}
    if scale_overrides:
        for family in ("space", "sizes", "type"):
            raw = scale_overrides.get(family)
            if isinstance(raw, dict) and raw:
                scales[family] = {str(k): str(v) for k, v in raw.items()}

    css = author_css.strip() if isinstance(author_css, str) and author_css.strip() else None

    pg = presentation_graph.to_dict() if hasattr(presentation_graph, "to_dict") else dict(presentation_graph)
    nodes_in = pg.get("nodes") or {}

    out = ResolvedDesign(
        mode=mode_key,
        tokens=modes,
        density=density_key,
        page=page,
        scales=scales,
        author_css=css,
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
