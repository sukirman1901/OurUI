from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceSpan:
    path: str
    start_line: int
    start_col: int
    end_line: int
    end_col: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Node:
    id: str
    kind: str
    span: SourceSpan
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list[str] = field(default_factory=list)
    provenance: list[str] = field(default_factory=list)
    revision: int = 0
    generation: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "kind": self.kind,
            "attributes": self.attributes,
            "children": self.children,
            "provenance": self.provenance,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def with_hash(self) -> Node:
        self.hash = self.compute_hash()
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "span": self.span.to_dict(),
            "attributes": self.attributes,
            "metadata": self.metadata,
            "children": list(self.children),
            "provenance": list(self.provenance),
            "revision": self.revision,
            "generation": self.generation,
            "hash": self.hash or self.compute_hash(),
        }


INTENT_KINDS = frozenset(
    {"Page", "Hero", "Section", "Shell", "Nav", "Footer", "Meta"}
)
PRESENTATION_KINDS = frozenset(
    {
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
        "Form",
        "Dialog",
        "Toast",
        "List",
        "Table",
        "Empty",
        "Spinner",
        "Alert",
        "Show",
        "When",
    }
)
KNOWN_KINDS = INTENT_KINDS | PRESENTATION_KINDS

# Authoring layout= intents (emit as shell classes; not Tailwind utilities)
SHELL_LAYOUT_INTENTS = frozenset(
    {"stack", "row", "split-2", "split-3", "split-sidebar", "grid"}
)

# Form controls (S2) — value/name on RTR attrs, not text children
FORM_CONTROL_KINDS = frozenset({"Input", "Select", "Toggle", "Slider"})

# Input type= enum (S2 + textarea for playground / multiline)
INPUT_TYPES = frozenset(
    {"text", "email", "password", "number", "search", "url", "tel", "textarea"}
)

# Alert severity (Phase U)
ALERT_SEVERITIES = frozenset({"info", "success", "warning", "danger"})

# Nav chrome (S3a / S6)
NAV_PLACEMENTS = frozenset(
    {"flow", "sticky-top", "fixed-top", "fixed-bottom", "overlay", "backdrop"}
)
NAV_TONES = frozenset({"solid", "glass"})
NAV_MENUS = frozenset({"none", "drawer"})

# Spacing / alignment intents (S3b / S4)
SPACE_INTENTS = frozenset({"none", "xs", "sm", "md", "lg", "xl", "2xl"})
ALIGN_INTENTS = frozenset({"start", "center", "end", "stretch"})
JUSTIFY_INTENTS = frozenset({"start", "center", "end", "between"})

# Motion vocabulary (ADR-012) — family.pattern + legacy S4m aliases
from ourui.design.motion import MOTION_INTENTS

# Canvas escape (S5)
CANVAS_MODES = frozenset({"gradient", "dither", "raymarch"})
REDUCED_MOTION = frozenset({"static", "off"})

# Image fit (S6)
IMAGE_FITS = frozenset({"cover", "contain", "fill", "none"})

THEME_ATTR_KEYS = frozenset({"variant", "color", "bg", "theme"})

# Shared passthrough for layout → render → presentation
_LAYOUT_CORE = (
    "title",
    "subtitle",
    "text",
    "variant",
    "color",
    "bg",
    "href",
    "external",
    "name",
    "placeholder",
    "type",
    "label",
    "value",
    "options",
    "min",
    "max",
    "step",
    "placement",
    "tone",
    "brand",
    "items",
    "actions",
    "links",
    "meta",
    "menu",
    "gap",
    "pad",
    "align",
    "justify",
    "motion",
    "mode",
    "config",
    "reduced_motion",
    "src",
    "srcdoc",
    "alt",
    "fit",
    "icon",
    "language",
    "description",
    "og",
    "disabled",
    "invalid",
    "loading",
    "action",
    "copy",
    "chrome",
    "helper",
    "open",
    "show",
    "columns",
    "rows",
    "severity",
    "message",
    "then",
    "else_",
)


def _layout_passthrough() -> tuple[str, ...]:
    from ourui.design.style_intents import STYLE_PASSTHROUGH

    seen: set[str] = set()
    out: list[str] = []
    for key in (*_LAYOUT_CORE, *STYLE_PASSTHROUGH):
        if key not in seen:
            seen.add(key)
            out.append(key)
    return tuple(out)


LAYOUT_PASSTHROUGH = _layout_passthrough()
