"""Completion and hover helpers for OurUI Python authoring."""

from __future__ import annotations

import re
from typing import Any

from ourui.theme import COLOR_TOKEN_NAMES, TOKEN_KEYS

UI_COMPONENTS: dict[str, str] = {
    "Page": "Intent domain root container.",
    "Hero": "Intent domain hero section.",
    "Section": "Intent domain content section.",
    "Button": "Presentation domain clickable control.",
    "Input": "Form control; name= collected into @server payload on button click.",
    "Select": "Dropdown form control; options= list of values or {value,label}.",
    "Toggle": "Checkbox form control; collected as boolean.",
    "Slider": "Range form control; min=/max=/step=.",
    "Text": "Presentation domain text node.",
    "Card": "Presentation domain card container.",
    "Grid": "Layout grid container.",
    "Link": "Presentation domain navigation anchor (href).",
    "Shell": "Intent domain layout region (layout=stack|row|split-3|grid).",
    "Nav": "Chrome bar; placement= + tone=solid|glass; brand/items/actions slots.",
    "Theme": "Design token overrides for --ourui-* CSS variables.",
}

TOP_LEVEL_KEYWORDS: dict[str, str] = {
    "State": "Reactive server-side state variable.",
    "server": "Decorator marking a server RPC handler.",
    "Component": "Base class for expandable UI components.",
}

_UI_PREFIX = re.compile(r"ui\.(\w*)$")
_TOP_LEVEL_PREFIX = re.compile(r"^\s*(\w*)$")
_UI_HOVER = re.compile(r"ui\.(\w+)")
_COLOR_KW = re.compile(r"""(?:color|variant|bg)\s*=\s*["'](\w*)$""")
_THEME_KW = re.compile(r"""(?:primary|primary_fg|bg|fg|muted|muted_fg|border|card|card_fg|accent|accent_fg|danger|danger_fg|radius|space_sm|space_md)\s*=\s*["']([^"']*)$""")


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
