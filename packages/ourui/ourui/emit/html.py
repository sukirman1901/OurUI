from __future__ import annotations

import html
from typing import Any

from ourui.emit.js import emit_js
from ourui.theme import COLOR_TOKEN_NAMES, default_tokens, emit_tokens_css

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
.ourui-root {
  font-family: system-ui, sans-serif;
  line-height: 1.5;
  background: var(--ourui-bg);
  color: var(--ourui-fg);
  min-height: 100vh;
  box-sizing: border-box;
  padding: var(--ourui-space-md);
}
.ourui-col { display: flex; flex-direction: column; gap: var(--ourui-space-md); }
.ourui-row { display: flex; flex-direction: row; gap: var(--ourui-space-md); }
.ourui-grid {
  display: grid;
  gap: var(--ourui-space-md);
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}
.ourui-card {
  padding: var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
}
.ourui-leaf { display: inline-block; }
button.ourui-control {
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  cursor: pointer;
  border-radius: var(--ourui-radius);
  border: 1px solid var(--ourui-border);
  background: var(--ourui-muted);
  color: var(--ourui-muted-fg);
}
button.ourui-tone-primary {
  background: var(--ourui-primary);
  color: var(--ourui-primary-fg);
  border-color: transparent;
}
button.ourui-tone-accent {
  background: var(--ourui-accent);
  color: var(--ourui-accent-fg);
  border-color: transparent;
}
button.ourui-tone-danger {
  background: var(--ourui-danger);
  color: var(--ourui-danger-fg);
  border-color: transparent;
}
button.ourui-tone-muted {
  background: var(--ourui-muted);
  color: var(--ourui-muted-fg);
}
"""


def _tone_name(attrs: dict[str, Any]) -> str | None:
    for key in ("color", "variant", "bg"):
        raw = attrs.get(key)
        if isinstance(raw, str) and raw in COLOR_TOKEN_NAMES:
            return raw
    return None


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
        tone = _tone_name(attrs)
        if tone:
            classes.append(f"ourui-tone-{tone}")
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
    if kind in {"Container", "Leaf", "Slot", "Drawing"}:
        return "div"
    return "div"


def _event_attrs(node: dict[str, Any]) -> str:
    events = node.get("attributes", {}).get("events") or {}
    parts: list[str] = []
    if "click" in events:
        parts.append(f' data-ourui-on-click="{html.escape(str(events["click"]))}"')
    return "".join(parts)


def _render_node(nid: str, nodes: dict[str, dict[str, Any]], indent: int) -> list[str]:
    node = nodes[nid]
    pad = "  " * indent
    kind = node["kind"]

    if kind == "Text":
        content = html.escape(str(node.get("attributes", {}).get("content", "")))
        slot = node.get("attributes", {}).get("slot", "")
        bind = node.get("attributes", {}).get("bind")
        slot_attr = f' data-slot="{html.escape(slot)}"' if slot else ""
        bind_attr = f' data-ourui-bind="{html.escape(str(bind))}"' if bind else ""
        return [f"{pad}<span{slot_attr}{bind_attr}>{content}</span>"]

    tag = _tag_for(node)
    classes = _classes_for(node)
    class_attr = f' class="{" ".join(classes)}"' if classes else ""
    role = node.get("attributes", {}).get("role", "")
    data_role = f' data-role="{html.escape(role)}"' if role else ""
    data_id = f' data-ourui-id="{html.escape(nid)}"'
    events = _event_attrs(node)

    children = node.get("children", [])
    attrs = f"{class_attr}{data_role}{data_id}{events}"

    if not children:
        return [f"{pad}<{tag}{attrs}></{tag}>"]

    lines = [f"{pad}<{tag}{attrs}>"]
    for child_id in children:
        if child_id not in nodes:
            continue
        lines.extend(_render_node(child_id, nodes, indent + 1))
    lines.append(f"{pad}</{tag}>")
    return lines


def apply_state_values(rtr: dict[str, Any], state_values: dict[str, Any] | None) -> dict[str, Any]:
    """Return a shallow-copied RTR with Text contents updated from live state."""
    if not state_values:
        return rtr
    import copy

    out = copy.deepcopy(rtr)
    for node in out["nodes"].values():
        if node.get("kind") != "Text":
            continue
        bind = node.get("attributes", {}).get("bind")
        if bind in state_values:
            node["attributes"]["content"] = "" if state_values[bind] is None else str(state_values[bind])
    return out


def emit_css(tokens: dict[str, dict[str, str]] | None = None) -> str:
    token_block = emit_tokens_css(tokens or default_tokens())
    return token_block + _BASE_CSS


def emit_html_document(
    rtr: dict[str, Any],
    *,
    title: str = "OurUI",
    state_values: dict[str, Any] | None = None,
    hmr: bool = False,
    tokens: dict[str, dict[str, str]] | None = None,
) -> str:
    """Emit a full HTML document from an RTR dict (HostNode tree only)."""
    rtr = apply_state_values(rtr, state_values)
    nodes = rtr["nodes"]
    roots = rtr["roots"]
    body_lines: list[str] = ['  <div class="ourui-root">']
    for root in roots:
        body_lines.extend(_render_node(root, nodes, 2))
    body_lines.append("  </div>")

    js = emit_js(rtr, hmr=hmr).rstrip("\n")
    css = emit_css(tokens).rstrip("\n")
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8" />',
        f"  <title>{html.escape(title)}</title>",
        "  <style>",
        css,
        "  </style>",
        "</head>",
        "<body>",
        *body_lines,
        "  <script>",
        js,
        "  </script>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)


def emit_bundle(
    rtr: dict[str, Any],
    *,
    title: str = "OurUI",
    tokens: dict[str, dict[str, str]] | None = None,
) -> dict[str, str]:
    """Serializable emit artifacts (I10): html + css + js."""
    return {
        "html": emit_html_document(rtr, title=title, tokens=tokens),
        "css": emit_css(tokens),
        "js": emit_js(rtr),
    }
