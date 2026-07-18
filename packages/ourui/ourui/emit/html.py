from __future__ import annotations

import html
from typing import Any

from ourui.emit.js import emit_js
from ourui.theme import COLOR_TOKEN_NAMES, emit_tokens_css

# Semantic role → HTML tag (emitter-only decision)
_ROLE_TAG: dict[str, str] = {
    "button": "button",
    "page": "main",
    "hero": "header",
    "section": "section",
    "shell": "div",
    "nav": "nav",
    "card": "div",
    "grid": "div",
    "text": "span",
    "link": "a",
    "input": "input",
    "select": "select",
    "toggle": "input",
    "slider": "input",
}

_BASE_CSS = """\
/* Host-private chrome (layout / structure). Not Design System knowledge.
   Tone colors come from Resolved Design (CSS vars + per-node rules). */
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
.ourui-row { display: flex; flex-direction: row; gap: var(--ourui-space-md); flex-wrap: wrap; }
.ourui-grid {
  display: grid;
  gap: var(--ourui-space-md);
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}
.ourui-shell-stack {
  display: flex;
  flex-direction: column;
  gap: var(--ourui-space-md);
  width: 100%;
}
.ourui-shell-split-3 {
  display: grid;
  gap: var(--ourui-space-md);
  grid-template-columns: minmax(11rem, 16rem) minmax(0, 1fr) minmax(11rem, 16rem);
  align-items: start;
  width: 100%;
}
@media (max-width: 767px) {
  .ourui-shell-split-3 { grid-template-columns: 1fr; }
}
.ourui-card {
  padding: var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
}
.ourui-leaf { display: inline-block; }
a.ourui-link {
  color: var(--ourui-primary);
  text-decoration: underline;
  text-underline-offset: 0.15em;
}
a.ourui-link:hover { filter: brightness(1.1); }
a.ourui-tone-primary { color: var(--ourui-primary); }
a.ourui-tone-accent { color: var(--ourui-accent); }
a.ourui-tone-danger { color: var(--ourui-danger); }
a.ourui-tone-muted { color: var(--ourui-muted-fg); }
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
.ourui-field {
  display: flex;
  flex-direction: column;
  gap: var(--ourui-space-sm);
  max-width: 24rem;
  width: 100%;
}
.ourui-field-label {
  font-size: 0.875rem;
  color: var(--ourui-muted-fg);
}
input.ourui-input {
  display: block;
  width: 100%;
  box-sizing: border-box;
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  font: inherit;
}
input.ourui-input:focus {
  outline: 2px solid var(--ourui-primary);
  outline-offset: 1px;
}
select.ourui-select {
  display: block;
  width: 100%;
  max-width: 24rem;
  box-sizing: border-box;
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  font: inherit;
}
.ourui-toggle-row {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-sm);
  max-width: 24rem;
}
input.ourui-toggle {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--ourui-primary);
}
input.ourui-slider {
  display: block;
  width: 100%;
  max-width: 24rem;
  accent-color: var(--ourui-primary);
}
.ourui-nav {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-md);
  flex-wrap: wrap;
  width: 100%;
  box-sizing: border-box;
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  z-index: 40;
}
.ourui-nav-brand {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-sm);
  font-weight: 600;
}
.ourui-nav-items {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-md);
  flex: 1 1 auto;
  flex-wrap: wrap;
}
.ourui-nav-actions {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-sm);
  margin-inline-start: auto;
}
.ourui-nav-solid {
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  border-bottom: 1px solid var(--ourui-border);
}
.ourui-nav-glass {
  background: color-mix(in srgb, var(--ourui-card) 72%, transparent);
  color: var(--ourui-card-fg);
  border-bottom: 1px solid var(--ourui-border);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
.ourui-nav-sticky-top {
  position: sticky;
  top: 0;
}
.ourui-nav-fixed-top {
  position: fixed;
  inset-inline: 0;
  top: 0;
}
.ourui-nav-fixed-bottom {
  position: fixed;
  inset-inline: 0;
  bottom: 0;
  border-bottom: none;
  border-top: 1px solid var(--ourui-border);
}
.ourui-nav-flow {
  position: static;
}
.ourui-nav-overlay {
  position: absolute;
  inset-inline: 0;
  top: 0;
}
.ourui-nav-backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.ourui-root:has(.ourui-nav-fixed-top) {
  padding-top: 3.75rem;
}
"""
# Tone classes above use CSS vars seeded from Resolved Design (Host Contract).
# Per-node rules from Resolved Design override for concrete fill/fg/radius/pad.
# Form control + Nav chrome is host-private layout — not Design System.

def _as_resolved_design(resolved_design: Any) -> dict[str, Any] | None:
    if resolved_design is None:
        return None
    if hasattr(resolved_design, "to_dict"):
        return resolved_design.to_dict()
    return dict(resolved_design)


def _tokens_from_resolved(rd: dict[str, Any]) -> dict[str, dict[str, str]]:
    tokens = rd.get("tokens") or {}
    return {
        "light": dict(tokens.get("light") or {}),
        "dark": dict(tokens.get("dark") or {}),
    }


def _emit_resolved_node_css(rd: dict[str, Any]) -> str:
    """Host maps Resolved Design node values → CSS (no Design System tables)."""
    lines: list[str] = []
    nodes = rd.get("nodes") or {}
    for nid in sorted(nodes):
        node = nodes[nid]
        role = node.get("role")
        resolved = node.get("resolved") or {}
        if role not in {"button", "link"}:
            continue
        fill = resolved.get("fill")
        fg = resolved.get("fg")
        if not fill and not fg:
            continue
        lines.append(f'[data-ourui-id="{nid}"] {{')
        if role == "button":
            if fill:
                lines.append(f"  background: {fill};")
            if fg:
                lines.append(f"  color: {fg};")
            if resolved.get("radius"):
                lines.append(f"  border-radius: {resolved['radius']};")
            pad_b = resolved.get("pad_block")
            pad_i = resolved.get("pad_inline")
            if pad_b and pad_i:
                lines.append(f"  padding: {pad_b} {pad_i};")
            lines.append("  border-color: transparent;")
        else:
            if fill:
                lines.append(f"  color: {fill};")
        lines.append("}")
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


def _tone_name(attrs: dict[str, Any]) -> str | None:
    for key in ("color", "variant", "bg"):
        raw = attrs.get(key)
        if isinstance(raw, str) and raw in COLOR_TOKEN_NAMES:
            return raw
    return None


def _is_external_href(href: str, external: Any) -> bool:
    if external is True:
        return True
    if external is False:
        return False
    return href.startswith("http://") or href.startswith("https://") or href.startswith("//")


def _link_attrs(attrs: dict[str, Any]) -> str:
    href = attrs.get("href")
    if not isinstance(href, str) or not href:
        return ""
    parts = [f' href="{html.escape(href, quote=True)}"']
    if _is_external_href(href, attrs.get("external")):
        parts.append(' target="_blank" rel="noopener noreferrer"')
    return "".join(parts)


def _classes_for(node: dict[str, Any]) -> list[str]:
    attrs = node.get("attributes", {})
    layout = attrs.get("layout", "none")
    shell = attrs.get("shell_layout")
    role = attrs.get("role", "")
    classes: list[str] = []
    if role != "nav":
        if shell == "split-3":
            classes.append("ourui-shell-split-3")
        elif shell == "stack":
            classes.append("ourui-shell-stack")
        elif layout == "vertical":
            classes.append("ourui-col")
        elif layout == "horizontal":
            classes.append("ourui-row")
        elif layout == "grid":
            classes.append("ourui-grid")
    if role == "card":
        classes.append("ourui-card")
    if role == "link":
        classes.append("ourui-link")
        tone = _tone_name(attrs)
        if tone:
            classes.append(f"ourui-tone-{tone}")
    if role == "button":
        classes.append("ourui-control")
        tone = _tone_name(attrs)
        if tone:
            classes.append(f"ourui-tone-{tone}")
    if role == "input":
        classes.append("ourui-input")
    if role == "select":
        classes.append("ourui-select")
    if role == "toggle":
        classes.append("ourui-toggle")
    if role == "slider":
        classes.append("ourui-slider")
    if role == "nav":
        classes.append("ourui-nav")
        placement = attrs.get("placement") or "sticky-top"
        tone = attrs.get("tone") or "solid"
        classes.append(f"ourui-nav-{placement}")
        classes.append(f"ourui-nav-{tone}")
    if (
        node["kind"] == "Leaf"
        and "ourui-control" not in classes
        and "ourui-link" not in classes
        and "ourui-input" not in classes
        and "ourui-select" not in classes
        and "ourui-toggle" not in classes
        and "ourui-slider" not in classes
        and "ourui-nav" not in classes
    ):
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


def _field_name_attrs(attrs: dict[str, Any]) -> list[str]:
    parts: list[str] = []
    name = attrs.get("name")
    if isinstance(name, str) and name:
        parts.append(f' name="{html.escape(name, quote=True)}"')
        parts.append(f' data-ourui-field="{html.escape(name, quote=True)}"')
    bind = attrs.get("bind")
    if isinstance(bind, str) and bind:
        parts.append(f' data-ourui-bind="{html.escape(bind, quote=True)}"')
    return parts


def _input_attrs(attrs: dict[str, Any]) -> str:
    parts = _field_name_attrs(attrs)
    input_type = attrs.get("type") or "text"
    if not isinstance(input_type, str) or not input_type:
        input_type = "text"
    parts.append(f' type="{html.escape(str(input_type), quote=True)}"')
    placeholder = attrs.get("placeholder")
    if isinstance(placeholder, str) and placeholder:
        parts.append(f' placeholder="{html.escape(placeholder, quote=True)}"')
    value = attrs.get("value")
    if value is not None and not isinstance(value, dict):
        parts.append(f' value="{html.escape(str(value), quote=True)}"')
    return "".join(parts)


def _select_attrs(attrs: dict[str, Any]) -> str:
    return "".join(_field_name_attrs(attrs))


def _toggle_attrs(attrs: dict[str, Any]) -> str:
    parts = _field_name_attrs(attrs)
    parts.append(' type="checkbox"')
    value = attrs.get("value")
    checked = False
    if isinstance(value, bool):
        checked = value
    elif value is not None and not isinstance(value, dict):
        checked = str(value).lower() in {"1", "true", "yes", "on"}
    if checked:
        parts.append(" checked")
    return "".join(parts)


def _slider_attrs(attrs: dict[str, Any]) -> str:
    parts = _field_name_attrs(attrs)
    parts.append(' type="range"')
    for key in ("min", "max", "step"):
        raw = attrs.get(key)
        if raw is not None and not isinstance(raw, dict):
            parts.append(f' {key}="{html.escape(str(raw), quote=True)}"')
    value = attrs.get("value")
    if value is not None and not isinstance(value, dict):
        parts.append(f' value="{html.escape(str(value), quote=True)}"')
    return "".join(parts)


def _wrap_field(pad: str, label: Any, control_lines: list[str], *, row: bool = False) -> list[str]:
    if not isinstance(label, str) or not label:
        return [f"{pad}{line}" if not line.startswith(pad) else line for line in control_lines]
    lab = html.escape(label)
    cls = "ourui-toggle-row" if row else "ourui-field"
    if row:
        # label after checkbox is common; put control then label text
        inner = [f"{pad}  {control_lines[0].lstrip()}", f'{pad}  <span class="ourui-field-label">{lab}</span>']
        return [f'{pad}<label class="{cls}">', *inner, f"{pad}</label>"]
    return [
        f'{pad}<label class="{cls}">',
        f'{pad}  <span class="ourui-field-label">{lab}</span>',
        *[f"{pad}  {line.lstrip()}" if line.strip().startswith("<") else line for line in control_lines],
        f"{pad}</label>",
    ]


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
    link = _link_attrs(node.get("attributes", {})) if role == "link" else ""
    node_attrs = node.get("attributes", {})

    if role == "input":
        field = _input_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        return _wrap_field(pad, node_attrs.get("label"), [f"<input{attrs} />"])

    if role == "select":
        field = _select_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        options = node_attrs.get("options") or []
        current = "" if node_attrs.get("value") is None else str(node_attrs.get("value"))
        opt_lines: list[str] = []
        if isinstance(options, list):
            for opt in options:
                if isinstance(opt, dict):
                    oval = str(opt.get("value", opt.get("label", "")))
                    olab = str(opt.get("label", oval))
                else:
                    oval = str(opt)
                    olab = oval
                sel = " selected" if oval == current else ""
                opt_lines.append(
                    f'{pad}  <option value="{html.escape(oval, quote=True)}"{sel}>{html.escape(olab)}</option>'
                )
        body = [f"{pad}<select{attrs}>", *opt_lines, f"{pad}</select>"]
        label = node_attrs.get("label")
        if isinstance(label, str) and label:
            return [
                f'{pad}<label class="ourui-field">',
                f'{pad}  <span class="ourui-field-label">{html.escape(label)}</span>',
                f"{pad}  <select{attrs}>",
                *[f"  {line}" if line.startswith(pad) else line for line in opt_lines],
                f"{pad}  </select>",
                f"{pad}</label>",
            ]
        return body

    if role == "toggle":
        field = _toggle_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        return _wrap_field(pad, node_attrs.get("label"), [f"<input{attrs} />"], row=True)

    if role == "slider":
        field = _slider_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        return _wrap_field(pad, node_attrs.get("label"), [f"<input{attrs} />"])

    if role == "nav":
        attrs = f"{class_attr}{data_role}{data_id}{events}"
        brand = node_attrs.get("brand")
        items = node_attrs.get("items") if isinstance(node_attrs.get("items"), list) else []
        actions = node_attrs.get("actions") if isinstance(node_attrs.get("actions"), list) else []
        slotted = set()
        if isinstance(brand, str):
            slotted.add(brand)
        slotted.update(i for i in items if isinstance(i, str))
        slotted.update(a for a in actions if isinstance(a, str))

        def _slot(title: str, ids: list[str]) -> list[str]:
            if not ids:
                return []
            out = [f'{pad}  <div class="ourui-nav-{title}">']
            for cid in ids:
                if cid in nodes:
                    out.extend(_render_node(cid, nodes, indent + 2))
            out.append(f"{pad}  </div>")
            return out

        lines = [f"{pad}<nav{attrs}>"]
        if isinstance(brand, str) and brand in nodes:
            lines.append(f'{pad}  <div class="ourui-nav-brand">')
            lines.extend(_render_node(brand, nodes, indent + 2))
            lines.append(f"{pad}  </div>")
        lines.extend(_slot("items", [i for i in items if isinstance(i, str)]))
        lines.extend(_slot("actions", [a for a in actions if isinstance(a, str)]))
        # Positional children not assigned to slots
        for child_id in node.get("children", []):
            if child_id in slotted or child_id not in nodes:
                continue
            lines.extend(_render_node(child_id, nodes, indent + 1))
        lines.append(f"{pad}</nav>")
        return lines

    children = node.get("children", [])
    attrs = f"{class_attr}{data_role}{data_id}{link}{events}"

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


def emit_css(*, resolved_design: Any) -> str:
    """Emit host CSS from Resolved Design (Host Contract — required)."""
    rd = _as_resolved_design(resolved_design)
    if rd is None:
        raise TypeError("resolved_design is required (Host Contract: RTR + Resolved Design)")
    token_block = emit_tokens_css(_tokens_from_resolved(rd))
    return token_block + _BASE_CSS + _emit_resolved_node_css(rd)


def emit_html_document(
    rtr: dict[str, Any],
    *,
    title: str = "OurUI",
    state_values: dict[str, Any] | None = None,
    hmr: bool = False,
    resolved_design: Any,
) -> str:
    """Emit HTML from Host Contract inputs: RTR + Resolved Design (both required)."""
    rtr = apply_state_values(rtr, state_values)
    nodes = rtr["nodes"]
    roots = rtr["roots"]
    body_lines: list[str] = ['  <div class="ourui-root">']
    for root in roots:
        body_lines.extend(_render_node(root, nodes, 2))
    body_lines.append("  </div>")

    js = emit_js(rtr, hmr=hmr).rstrip("\n")
    css = emit_css(resolved_design=resolved_design).rstrip("\n")
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
    resolved_design: Any,
) -> dict[str, str]:
    """Serializable emit artifacts (I10): html + css + js."""
    return {
        "html": emit_html_document(
            rtr, title=title, resolved_design=resolved_design
        ),
        "css": emit_css(resolved_design=resolved_design),
        "js": emit_js(rtr),
    }
