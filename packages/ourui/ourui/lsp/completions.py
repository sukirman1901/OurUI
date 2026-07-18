"""Completion and hover helpers for OurUI Python authoring."""

from __future__ import annotations

import re
from typing import Any

from ourui.theme import COLOR_TOKEN_NAMES, TOKEN_KEYS

UI_COMPONENTS: dict[str, str] = {
    "Page": "Intent domain root container.",
    "Hero": "Intent domain hero section; pad=/motion=family.pattern.",
    "Section": "Intent domain content section; gap=/pad=/align=/motion=family.pattern.",
    "Button": "Presentation domain clickable control; motion=press.scale.",
    "Input": "Form control; name= into @server payload; type=text|…|textarea.",
    "Select": "Dropdown form control; options= list of values or {value,label}.",
    "Toggle": "Checkbox form control; collected as boolean.",
    "Slider": "Range form control; min=/max=/step=.",
    "Text": "Presentation domain text; motion=text.word-reveal|text.fade-up|….",
    "Card": "Presentation domain card container.",
    "Grid": "Layout grid container.",
    "Link": "Presentation domain navigation anchor (href).",
    "Shell": "Layout region (layout=stack|row|split-2|split-3|split-sidebar|grid); gap=/pad=/width=/grow=/grid_cols= style intents.",
    "Nav": "Chrome bar; placement= + tone=solid|glass; menu=drawer; brand/items/actions.",
    "Footer": "Page footer; brand=/links=/meta= slots.",
    "ThemeToggle": "Client control that toggles .dark on <html>.",
    "Theme": "Theme roles: density=, page={...}, css= author sheet, color overrides, space=/sizes=/type= scale dicts.",
    "Canvas": "WebGL escape; mode=gradient|dither|raymarch (Plasma.init).",
    "Frame": "Host escape iframe preview; bind=/srcdoc= HTML document string.",
    "Image": "Image; src=/alt=/fit=cover|contain.",
    "Icon": "Inline icon (Reicon-style name=).",
    "Meta": "Document head title/description/og=.",
    "Code": "Code block; text= + language=.",
    "CopyButton": "Clipboard button; copy= payload.",
    "Menu": "Dropdown menu; items= slot.",
    "Form": "Form shell; on_submit= collects fields.",
    "Dialog": "Modal; open= State; title=/actions=.",
    "Toast": "Ephemeral toast; text= + open=.",
    "List": "Semantic list; items= list or State (dynamic).",
    "Table": "Semantic table; columns= + rows= list or State.",
    "Empty": "Empty state; title=/subtitle=.",
    "Spinner": "Loading indicator.",
    "Alert": "Alert; severity=info|success|warning|danger; text= may bind State.",
    "Show": "Conditional visibility; show= State|bool; children always in DOM.",
    "When": "Branching visibility; show= + then= + else_= (both branches emitted).",
}


TOP_LEVEL_KEYWORDS: dict[str, str] = {
    "State": "Reactive server-side state variable.",
    "Derived": "Draft computed value from a zero-arg callable.",
    "server": "Decorator marking a server RPC handler.",
    "Component": "Base class for expandable UI components.",
}

_UI_PREFIX = re.compile(r"ui\.(\w*)$")
_TOP_LEVEL_PREFIX = re.compile(r"^\s*(\w*)$")
_UI_HOVER = re.compile(r"ui\.(\w+)")
_COLOR_KW = re.compile(r"""(?:color|variant|bg)\s*=\s*["'](\w*)$""")
_THEME_KW = re.compile(r"""(?:primary|primary_fg|bg|fg|muted|muted_fg|border|card|card_fg|accent|accent_fg|danger|danger_fg|radius|space_sm|space_md)\s*=\s*["']([^"']*)$""")
_STYLE_KW = re.compile(
    r"""(?P<prop>width|height|min_width|max_width|size|pad|pad_x|pad_y|gap|space_x|space_y|"""
    r"""scroll_m|scroll_p|scroll_mt|scroll_pt|grow|shrink|basis|"""
    r"""grid_cols|col_span|text|weight|leading|radius|opacity|blur|z|overflow|pos|"""
    r"""ring|ring_color|divide|divide_w|divide_color|bg_gradient|gradient_from|gradient_to|"""
    r"""caret|caret_color|sr_only|appearance|color_scheme|field_sizing|"""
    r"""scrollbar_width|scrollbar_gutter|scrollbar_color|tab_size|text_indent|zoom|backface|"""
    r"""outline|outline_color|outline_offset|accent|accent_color|font_numeric|"""
    r"""font_stretch|font_feature|"""
    r"""placeholder_color|selection_bg|selection_color|"""
    r"""mix_blend|backdrop_blend|mask|bg_image|container|"""
    r"""before_content|after_content|"""
    r"""hide_below|show_below)\s*=\s*["'](?P<val>[^"']*)$"""
)
_THEME_ROLES = ("primary", "accent", "muted", "danger", "border", "fg", "bg")
_GRAD_DIRS = ("to-t", "to-tr", "to-r", "to-br", "to-b", "to-bl", "to-l", "to-tl")

_SIZE_VALUES = (
    "auto",
    "full",
    "screen",
    "xs",
    "sm",
    "md",
    "lg",
    "xl",
    "2xl",
    "3xl",
    "4xl",
    "5xl",
    "6xl",
    "7xl",
    "1/2",
    "1/3",
    "2/3",
    "1/4",
    "3/4",
)
_SPACE_VALUES = ("0", "px", "1", "2", "3", "4", "5", "6", "8", "10", "12", "16", "none", "xs", "sm", "md", "lg", "xl", "2xl")
_TEXT_VALUES = ("xs", "sm", "md", "base", "lg", "xl", "2xl", "3xl", "4xl", "display")
_BREAK_VALUES = ("md", "lg")


def _style_value_items(prop: str, prefix: str) -> list[dict[str, Any]]:
    if prop in {"width", "height", "min_width", "max_width", "size", "basis"}:
        values = _SIZE_VALUES
    elif prop in {
        "pad",
        "pad_x",
        "pad_y",
        "gap",
        "space_x",
        "space_y",
        "scroll_m",
        "scroll_p",
        "scroll_mt",
        "scroll_pt",
    }:
        values = _SPACE_VALUES
    elif prop == "text":
        values = _TEXT_VALUES
    elif prop in {"hide_below", "show_below"}:
        values = _BREAK_VALUES
    elif prop in {"grow", "shrink"}:
        values = ("0", "1")
    elif prop == "grid_cols" or prop == "col_span":
        values = tuple(str(i) for i in range(1, 13))
    elif prop == "weight":
        values = ("normal", "medium", "semibold", "bold")
    elif prop == "leading":
        values = ("tight", "normal", "relaxed")
    elif prop == "radius":
        values = ("none", "sm", "md", "lg", "xl", "full")
    elif prop == "opacity":
        values = ("0", "50", "75", "100")
    elif prop == "blur":
        values = ("none", "sm", "md", "lg")
    elif prop == "z":
        values = ("auto", "0", "10", "20", "30", "40", "50")
    elif prop == "overflow":
        values = ("auto", "hidden", "clip", "scroll", "visible")
    elif prop == "pos":
        values = ("static", "relative", "absolute", "fixed", "sticky")
    elif prop == "ring":
        values = ("0", "1", "2", "4", "8", "ring")
    elif prop in {
        "ring_color",
        "divide_color",
        "caret",
        "caret_color",
        "gradient_from",
        "gradient_to",
        "outline_color",
        "accent",
        "accent_color",
        "placeholder_color",
        "selection_bg",
        "selection_color",
    }:
        values = _THEME_ROLES
    elif prop == "divide":
        values = ("x", "y")
    elif prop == "divide_w":
        values = ("0", "1", "2", "4", "8")
    elif prop == "outline":
        values = ("none", "hidden", "0", "1", "2", "4", "8", "outline")
    elif prop == "outline_offset":
        values = ("0", "1", "2", "4", "8")
    elif prop == "font_numeric":
        values = (
            "normal",
            "ordinal",
            "slashed-zero",
            "lining",
            "oldstyle",
            "proportional",
            "tabular",
            "diagonal-fractions",
            "stacked-fractions",
        )
    elif prop == "font_stretch":
        values = (
            "ultra-condensed",
            "extra-condensed",
            "condensed",
            "semi-condensed",
            "normal",
            "semi-expanded",
            "expanded",
            "extra-expanded",
            "ultra-expanded",
        )
    elif prop == "font_feature":
        values = (
            "normal",
            "liga",
            "no-liga",
            "dlig",
            "no-dlig",
            "hist",
            "calt",
            "no-calt",
            "ss01",
            "ss02",
            "ss03",
            "ss04",
            "cv01",
            "cv02",
            "cv03",
            "cv04",
            "smcp",
        )
    elif prop in {"mix_blend", "backdrop_blend"}:
        values = (
            "normal",
            "multiply",
            "screen",
            "overlay",
            "darken",
            "lighten",
            "color-dodge",
            "color-burn",
            "hard-light",
            "soft-light",
            "difference",
            "exclusion",
            "hue",
            "saturation",
            "color",
            "luminosity",
            "plus-darker",
            "plus-lighter",
        )
    elif prop == "mask":
        values = ("none", "fade-t", "fade-r", "fade-b", "fade-l", "fade-x", "fade-y", "radial")
    elif prop == "bg_image":
        values = ("none",)
    elif prop == "container":
        values = ("normal", "inline-size")
    elif prop in {"before_content", "after_content"}:
        values = ("none", "empty", "open-quote", "close-quote")
    elif prop == "bg_gradient":
        values = _GRAD_DIRS
    elif prop == "sr_only":
        values = ("true", "false")
    elif prop == "appearance":
        values = ("none", "auto")
    elif prop == "color_scheme":
        values = ("normal", "light", "dark", "light-dark")
    elif prop == "field_sizing":
        values = ("content", "fixed")
    elif prop == "scrollbar_width":
        values = ("auto", "thin", "none")
    elif prop == "scrollbar_gutter":
        values = ("auto", "stable", "stable-both")
    elif prop == "scrollbar_color":
        values = ("auto",) + _THEME_ROLES
    elif prop == "tab_size":
        values = ("0", "2", "4", "8")
    elif prop == "text_indent":
        values = _SPACE_VALUES
    elif prop == "zoom":
        values = ("0", "50", "75", "90", "95", "100", "105", "110", "125", "150")
    elif prop == "backface":
        values = ("visible", "hidden")
    else:
        values = ()
    items: list[dict[str, Any]] = []
    for name in values:
        if str(name).startswith(prefix):
            items.append(
                _completion_item(
                    str(name),
                    detail=f"{prop}={name}",
                    documentation=f"Style intent value for {prop}= (ADR-013).",
                    kind=12,
                )
            )
    return items


def _completion_item(label: str, *, detail: str, documentation: str, kind: int) -> dict[str, Any]:
    return {
        "label": label,
        "kind": kind,
        "detail": detail,
        "documentation": documentation,
    }


def _ui_completion_items(prefix: str = "") -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name, doc in UI_COMPONENTS.items():
        if name.startswith(prefix):
            items.append(
                _completion_item(
                    name,
                    detail=f"ui.{name}",
                    documentation=doc,
                    kind=7,
                )
            )
    return items


def _top_level_completion_items(prefix: str = "") -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name, doc in TOP_LEVEL_KEYWORDS.items():
        if name.startswith(prefix):
            items.append(
                _completion_item(
                    name,
                    detail=name,
                    documentation=doc,
                    kind=14,
                )
            )
    return items


def _token_completion_items(prefix: str = "") -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name in COLOR_TOKEN_NAMES:
        if name.startswith(prefix):
            items.append(
                _completion_item(
                    name,
                    detail=f"token:{name}",
                    documentation=f"Maps to var(--ourui-{name.replace('_', '-')}).",
                    kind=12,
                )
            )
    return items


def _line_prefix(text: str, line: int, character: int) -> str:
    lines = text.splitlines()
    if line < 0 or line >= len(lines):
        return ""
    return lines[line][: max(0, character)]


def get_completions(text: str, line: int, character: int) -> list[dict[str, Any]]:
    """Return LSP completion items for the given cursor position."""
    prefix = _line_prefix(text, line, character)

    color_match = _COLOR_KW.search(prefix)
    if color_match is not None:
        return _token_completion_items(color_match.group(1))

    style_match = _STYLE_KW.search(prefix)
    if style_match is not None:
        return _style_value_items(style_match.group("prop"), style_match.group("val"))

    ui_match = _UI_PREFIX.search(prefix)
    if ui_match is not None:
        return _ui_completion_items(ui_match.group(1))

    top_match = _TOP_LEVEL_PREFIX.match(prefix)
    if top_match is not None and "." not in prefix:
        return _top_level_completion_items(top_match.group(1))

    return []


def _token_at(text: str, line: int, character: int) -> tuple[str, int, int]:
    lines = text.splitlines()
    if line < 0 or line >= len(lines):
        return "", character, character
    line_text = lines[line]
    start = min(character, len(line_text))
    end = start
    while start > 0 and (line_text[start - 1].isalnum() or line_text[start - 1] in "._"):
        start -= 1
    while end < len(line_text) and (line_text[end].isalnum() or line_text[end] in "._"):
        end += 1
    return line_text[start:end], start, end


def get_hover(text: str, line: int, character: int) -> dict[str, Any] | None:
    """Return an LSP hover payload for ui.* identifiers, or None."""
    token, start, end = _token_at(text, line, character)
    match = _UI_HOVER.fullmatch(token)
    if match is None:
        return None

    name = match.group(1)
    doc = UI_COMPONENTS.get(name)
    if doc is None:
        return None

    return {
        "contents": {"kind": "markdown", "value": f"**ui.{name}** — {doc}"},
        "range": {
            "start": {"line": line, "character": start},
            "end": {"line": line, "character": end},
        },
    }


# Re-export for tests / editors that want the key list
THEME_TOKEN_KEYS = TOKEN_KEYS
