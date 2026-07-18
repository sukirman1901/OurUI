from __future__ import annotations

import html
from typing import Any

# Semantic role → HTML tag (emitter-only decision)
_ROLE_TAG: dict[str, str] = {
    "button": "button",
    "page": "main",
    "hero": "header",
    "section": "section",
    "card": "div",
    "grid": "div",
    "text": "span",
}

_BASE_CSS = """\
.ourui-root { font-family: system-ui, sans-serif; line-height: 1.5; }
.ourui-col { display: flex; flex-direction: column; gap: 0.75rem; }
.ourui-row { display: flex; flex-direction: row; gap: 0.75rem; }
.ourui-grid { display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr)); }
.ourui-card { padding: 1rem; border: 1px solid #d4d4d8; border-radius: 0.5rem; }
.ourui-leaf { display: inline-block; }
button.ourui-control { padding: 0.5rem 1rem; cursor: pointer; }
"""


def _classes_for(node: dict[str, Any]) -> list[str]:
    attrs = node.get("attributes", {})
    layout = attrs.get("layout", "none")
    role = attrs.get("role", "")
    classes: list[str] = []
    if layout == "vertical":
        classes.append("ourui-col")
    elif layout == "horizontal":
        classes.append("ourui-row")
    elif layout == "grid":
        classes.append("ourui-grid")
    if role == "card":
        classes.append("ourui-card")
    if role == "button":
        classes.append("ourui-control")
    if node["kind"] == "Leaf" and "ourui-control" not in classes:
        classes.append("ourui-leaf")
    return classes


def _tag_for(node: dict[str, Any]) -> str:
    kind = node["kind"]
    if kind == "Text":
        return "span"
    role = node.get("attributes", {}).get("role", "")
    if role in _ROLE_TAG:
        return _ROLE_TAG[role]
    if kind == "Container":
        return "div"
    if kind == "Leaf":
        return "div"
    if kind == "Slot":
        return "div"
    if kind == "Drawing":
        return "div"
    return "div"


def _render_node(nid: str, nodes: dict[str, dict[str, Any]], indent: int) -> list[str]:
    node = nodes[nid]
    pad = "  " * indent
    kind = node["kind"]

    if kind == "Text":
        content = html.escape(str(node.get("attributes", {}).get("content", "")))
        slot = node.get("attributes", {}).get("slot", "")
        slot_attr = f' data-slot="{html.escape(slot)}"' if slot else ""
        return [f"{pad}<span{slot_attr}>{content}</span>"]

    tag = _tag_for(node)
    classes = _classes_for(node)
    class_attr = f' class="{" ".join(classes)}"' if classes else ""
    role = node.get("attributes", {}).get("role", "")
    data_role = f' data-role="{html.escape(role)}"' if role else ""
    data_id = f' data-ourui-id="{html.escape(nid)}"'

    children = node.get("children", [])
    open_tag = f"{pad}<{tag}{class_attr}{data_role}{data_id}>"
    close_tag = f"{pad}</{tag}>"

    if not children:
        return [f"{pad}<{tag}{class_attr}{data_role}{data_id}></{tag}>"]

    lines = [open_tag]
    for child_id in children:
        if child_id not in nodes:
            continue
        lines.extend(_render_node(child_id, nodes, indent + 1))
    lines.append(close_tag)
    return lines


def emit_html_document(rtr: dict[str, Any], *, title: str = "OurUI") -> str:
    """Emit a full HTML document from an RTR dict (HostNode tree only)."""
    nodes = rtr["nodes"]
    roots = rtr["roots"]
    body_lines: list[str] = ['  <div class="ourui-root">']
    for root in roots:
        body_lines.extend(_render_node(root, nodes, 2))
    body_lines.append("  </div>")

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8" />',
        f"  <title>{html.escape(title)}</title>",
        "  <style>",
        _BASE_CSS.rstrip("\n"),
        "  </style>",
        "</head>",
        "<body>",
        *body_lines,
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)


def emit_css() -> str:
    return _BASE_CSS


def emit_bundle(rtr: dict[str, Any], *, title: str = "OurUI") -> dict[str, str]:
    """Serializable emit artifacts (I10): html + css. JS deferred."""
    return {
        "html": emit_html_document(rtr, title=title),
        "css": emit_css(),
        "js": "",  # Phase E minimal — no JS yet
    }
