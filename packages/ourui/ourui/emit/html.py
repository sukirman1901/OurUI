from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from ourui.emit.js import emit_js
from ourui.theme import COLOR_TOKEN_NAMES, emit_tokens_css

_PLASMA_ENGINE = (Path(__file__).resolve().parent.parent / "host" / "plasma" / "plasma-engine.js").read_text(
    encoding="utf-8"
)

# Semantic role → HTML tag (emitter-only decision)
_ROLE_TAG: dict[str, str] = {
    "button": "button",
    "page": "main",
    "hero": "header",
    "section": "section",
    "shell": "div",
    "nav": "nav",
    "footer": "footer",
    "card": "div",
    "grid": "div",
    "text": "span",
    "link": "a",
    "input": "input",
    "select": "select",
    "toggle": "input",
    "slider": "input",
    "theme-toggle": "button",
    "canvas": "canvas",
    "frame": "iframe",
    "image": "img",
    "icon": "span",
    "code": "pre",
    "copy-button": "button",
    "menu": "div",
    "meta": "div",
}

_BASE_CSS = """\
/* Host-private chrome (layout / structure). Not Design System knowledge.
   Tone colors come from Resolved Design (CSS vars + per-node rules). */
.ourui-root {
  font-family: var(--ourui-font-sans);
  font-size: var(--ourui-text-md);
  line-height: var(--ourui-leading-normal);
  background: var(--ourui-bg);
  color: var(--ourui-fg);
  min-height: 100vh;
  box-sizing: border-box;
  padding: 0;
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
.ourui-shell-row {
  display: flex;
  flex-direction: row;
  gap: var(--ourui-space-md);
  flex-wrap: wrap;
  width: 100%;
}
.ourui-shell-split-2 {
  display: grid;
  gap: 0;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  align-items: stretch;
  width: 100%;
  min-height: calc(100vh - 3.25rem);
  border-top: 1px solid var(--ourui-border);
  background: var(--ourui-card);
}
.ourui-shell-split-2 > *:first-child {
  border-inline-end: 1px solid var(--ourui-border);
  background: var(--ourui-card);
  min-width: 0;
}
.ourui-shell-split-2 > *:last-child {
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.ourui-shell-split-3 {
  display: grid;
  gap: var(--ourui-space-md);
  grid-template-columns: minmax(11rem, 16rem) minmax(0, 1fr) minmax(11rem, 16rem);
  align-items: start;
  width: 100%;
}
.ourui-shell-split-sidebar {
  display: grid;
  gap: var(--ourui-space-md);
  grid-template-columns: minmax(11rem, 16rem) minmax(0, 1fr);
  align-items: start;
  width: 100%;
}
@media (max-width: 767px) {
  .ourui-shell-split-2,
  .ourui-shell-split-3,
  .ourui-shell-split-sidebar { grid-template-columns: 1fr; }
}
.ourui-gap-none { gap: 0 !important; }
.ourui-gap-xs { gap: var(--ourui-space-xs) !important; }
.ourui-gap-sm { gap: var(--ourui-space-sm) !important; }
.ourui-gap-md { gap: var(--ourui-space-md) !important; }
.ourui-gap-lg { gap: var(--ourui-space-lg) !important; }
.ourui-gap-xl { gap: var(--ourui-space-xl) !important; }
.ourui-gap-2xl { gap: var(--ourui-space-2xl) !important; }
.ourui-pad-none { padding: 0 !important; }
.ourui-pad-xs { padding: var(--ourui-space-xs) !important; }
.ourui-pad-sm { padding: var(--ourui-space-sm) !important; }
.ourui-pad-md { padding: var(--ourui-space-md) !important; }
.ourui-pad-lg { padding: var(--ourui-space-lg) !important; }
.ourui-pad-xl { padding: var(--ourui-space-xl) !important; }
.ourui-pad-2xl { padding: var(--ourui-space-2xl) !important; }
.ourui-align-start { align-items: flex-start !important; }
.ourui-align-center { align-items: center !important; }
.ourui-align-end { align-items: flex-end !important; }
.ourui-align-stretch { align-items: stretch !important; }
.ourui-justify-start { justify-content: flex-start !important; }
.ourui-justify-center { justify-content: center !important; }
.ourui-justify-end { justify-content: flex-end !important; }
.ourui-justify-between { justify-content: space-between !important; }
.ourui-card {
  padding: var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  box-shadow: var(--ourui-elev-1);
}
.ourui-leaf { display: inline-block; }
[data-role="hero"] {
  padding-block: var(--ourui-space-2xl);
  padding-inline: var(--ourui-space-md);
  position: relative;
  z-index: 1;
}
[data-role="hero"] [data-slot="title"],
[data-role="hero"] > span[data-slot="title"] {
  display: block;
  font-family: var(--ourui-font-display);
  font-size: var(--ourui-text-2xl);
  line-height: var(--ourui-leading-tight);
  font-weight: 600;
}
[data-role="hero"] [data-slot="subtitle"] {
  display: block;
  margin-top: var(--ourui-space-sm);
  font-size: var(--ourui-text-lg);
  color: var(--ourui-muted-fg);
  max-width: 36rem;
}
[data-role="section"] {
  padding-block: var(--ourui-space-xl);
}
[data-role="section"] [data-slot="title"] {
  display: block;
  font-family: var(--ourui-font-display);
  font-size: var(--ourui-text-xl);
  margin-bottom: var(--ourui-space-md);
}
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
button.ourui-control,
button.ourui-theme-toggle,
button.ourui-copy-button,
button.ourui-nav-menu-btn {
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  cursor: pointer;
  border-radius: var(--ourui-radius);
  border: 1px solid var(--ourui-border);
  background: var(--ourui-muted);
  color: var(--ourui-muted-fg);
  font: inherit;
  box-shadow: var(--ourui-elev-0);
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
button.ourui-control:disabled,
button.ourui-control[aria-busy="true"],
input.ourui-input:disabled,
select.ourui-select:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
input.ourui-input[aria-invalid="true"],
select.ourui-select[aria-invalid="true"] {
  border-color: var(--ourui-danger);
}
.ourui-field {
  display: flex;
  flex-direction: column;
  gap: var(--ourui-space-sm);
  max-width: 24rem;
  width: 100%;
}
.ourui-field-label {
  font-size: var(--ourui-text-sm);
  color: var(--ourui-muted-fg);
}
input.ourui-input,
textarea.ourui-input {
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
textarea.ourui-input {
  min-height: 18rem;
  resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.8125rem;
  line-height: 1.55;
  tab-size: 2;
  white-space: pre;
  border-radius: 0;
  border: none;
  border-top: 1px solid var(--ourui-border);
  flex: 1 1 auto;
}
input.ourui-input:focus,
textarea.ourui-input:focus {
  outline: 2px solid var(--ourui-primary);
  outline-offset: 1px;
}
.ourui-frame {
  display: block;
  width: 100%;
  min-height: 22rem;
  flex: 1 1 auto;
  border: none;
  border-top: 1px solid var(--ourui-border);
  background: var(--ourui-card);
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
  box-shadow: var(--ourui-elev-1);
}
.ourui-nav-brand {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-sm);
  font-weight: 600;
  font-family: var(--ourui-font-display);
  font-size: var(--ourui-text-lg);
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
.ourui-nav-sticky-top { position: sticky; top: 0; }
.ourui-nav-fixed-top { position: fixed; inset-inline: 0; top: 0; }
.ourui-nav-fixed-bottom {
  position: fixed;
  inset-inline: 0;
  bottom: 0;
  border-bottom: none;
  border-top: 1px solid var(--ourui-border);
}
.ourui-nav-flow { position: static; }
.ourui-nav-overlay { position: absolute; inset-inline: 0; top: 0; }
.ourui-nav-backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.ourui-root:has(.ourui-nav-fixed-top) { padding-top: 3.75rem; }
.ourui-nav-menu-btn { display: none; }
.ourui-nav-drawer {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--ourui-bg) 88%, transparent);
  padding: var(--ourui-space-lg);
}
.ourui-nav-drawer[data-open="true"] {
  display: flex;
  flex-direction: column;
  gap: var(--ourui-space-md);
}
.ourui-nav-drawer-panel {
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  border-radius: var(--ourui-radius);
  padding: var(--ourui-space-md);
  box-shadow: var(--ourui-elev-3);
  display: flex;
  flex-direction: column;
  gap: var(--ourui-space-md);
  max-width: 20rem;
}
@media (max-width: 767px) {
  .ourui-nav[data-menu="drawer"] .ourui-nav-items { display: none; }
  .ourui-nav[data-menu="drawer"] .ourui-nav-menu-btn { display: inline-flex; }
  button.ourui-tone-primary,
  a.ourui-link.ourui-tone-primary {
    width: 100%;
    text-align: center;
    display: inline-block;
    box-sizing: border-box;
  }
}
.ourui-footer {
  display: flex;
  flex-wrap: wrap;
  gap: var(--ourui-space-lg);
  padding-block: var(--ourui-space-xl);
  margin-top: var(--ourui-space-2xl);
  border-top: 1px solid var(--ourui-border);
  color: var(--ourui-muted-fg);
  font-size: var(--ourui-text-sm);
}
.ourui-footer-brand { font-weight: 600; color: var(--ourui-fg); }
.ourui-footer-links,
.ourui-footer-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--ourui-space-md);
}
.ourui-canvas {
  display: block;
  width: 100%;
  min-height: 16rem;
  height: 100%;
  border-radius: var(--ourui-radius);
  background: var(--ourui-muted);
  box-shadow: var(--ourui-elev-2);
}
.ourui-canvas-backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  min-height: 100%;
  border-radius: 0;
  pointer-events: none;
}
.ourui-canvas-static {
  background:
    radial-gradient(ellipse at 30% 20%, color-mix(in srgb, var(--ourui-primary) 45%, transparent), transparent 55%),
    radial-gradient(ellipse at 70% 80%, color-mix(in srgb, var(--ourui-accent) 35%, transparent), transparent 50%),
    var(--ourui-bg);
}
.ourui-hero-wrap { position: relative; overflow: hidden; }
img.ourui-image {
  display: block;
  max-width: 100%;
  height: auto;
  border-radius: var(--ourui-radius);
}
img.ourui-fit-cover { object-fit: cover; width: 100%; height: 100%; }
img.ourui-fit-contain { object-fit: contain; width: 100%; height: 100%; }
img.ourui-fit-fill { object-fit: fill; width: 100%; height: 100%; }
.ourui-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25em;
  height: 1.25em;
  vertical-align: -0.15em;
}
.ourui-icon svg { width: 100%; height: 100%; fill: currentColor; }
.ourui-code {
  display: block;
  overflow: auto;
  padding: var(--ourui-space-md);
  border-radius: 0;
  background: #ffffff;
  color: var(--ourui-fg);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.8125rem;
  box-shadow: none;
  white-space: pre;
  min-height: 16rem;
  border: none;
  border-top: 1px solid var(--ourui-border);
  line-height: 1.55;
  tab-size: 2;
}
.dark .ourui-code {
  background: #0c0c0e;
}
.ourui-playground-tabs a.ourui-link {
  text-decoration: none;
  color: var(--ourui-muted-fg);
  font-weight: 500;
  font-size: var(--ourui-text-sm);
}
.ourui-playground-tabs a.ourui-tone-primary {
  color: var(--ourui-fg);
  box-shadow: inset 0 -2px 0 var(--ourui-fg);
  padding-bottom: 0.2rem;
}
.ourui-file-tab-row {
  display: flex;
  align-items: center;
  gap: var(--ourui-space-sm);
  padding: var(--ourui-space-sm) var(--ourui-space-md) 0;
  border-bottom: 1px solid var(--ourui-border);
  background: var(--ourui-bg);
}
.ourui-file-tab {
  display: inline-flex;
  align-items: center;
  gap: var(--ourui-space-xs);
  padding: var(--ourui-space-sm) var(--ourui-space-md);
  border: 1px solid var(--ourui-border);
  border-bottom-color: var(--ourui-card);
  margin-bottom: -1px;
  border-radius: var(--ourui-radius) var(--ourui-radius) 0 0;
  background: var(--ourui-card);
  font-size: var(--ourui-text-sm);
  font-weight: 500;
}
.ourui-result-hero {
  font-family: var(--ourui-font-sans);
  font-size: var(--ourui-text-2xl);
  font-weight: 600;
  line-height: var(--ourui-leading-tight);
  margin: 0;
}
.ourui-nav {
  box-shadow: none !important;
}
@media (max-width: 767px) {
  .ourui-shell-split-2 > *:first-child {
    border-inline-end: none;
    border-bottom: 1px solid var(--ourui-border);
  }
}
.ourui-menu {
  position: relative;
  display: inline-block;
}
.ourui-menu-panel {
  display: none;
  position: absolute;
  right: 0;
  top: calc(100% + 0.25rem);
  min-width: 10rem;
  padding: var(--ourui-space-sm);
  background: var(--ourui-card);
  color: var(--ourui-card-fg);
  border: 1px solid var(--ourui-border);
  border-radius: var(--ourui-radius);
  box-shadow: var(--ourui-elev-2);
  z-index: 30;
  flex-direction: column;
  gap: var(--ourui-space-xs);
}
.ourui-menu[data-open="true"] .ourui-menu-panel { display: flex; }
.ourui-motion-enter { animation: ourui-enter 0.45s ease-out both; }
.ourui-motion-reveal { animation: ourui-reveal 0.55s ease-out both; }
.ourui-motion-press:active { transform: scale(0.97); transition: transform 0.12s ease; }
@keyframes ourui-enter {
  from { opacity: 0; transform: translateY(0.5rem); }
  to { opacity: 1; transform: none; }
}
@keyframes ourui-reveal {
  from { opacity: 0; clip-path: inset(0 0 100% 0); }
  to { opacity: 1; clip-path: inset(0 0 0 0); }
}
@media (prefers-reduced-motion: reduce) {
  .ourui-motion-enter,
  .ourui-motion-reveal { animation: none; }
  .ourui-motion-press:active { transform: none; }
}
.ourui-meta-host { display: none; }
"""


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


def _layout_intent_classes(attrs: dict[str, Any]) -> list[str]:
    classes: list[str] = []
    shell = attrs.get("shell_layout")
    if shell == "split-3":
        classes.append("ourui-shell-split-3")
    elif shell == "split-2":
        classes.append("ourui-shell-split-2")
    elif shell == "split-sidebar":
        classes.append("ourui-shell-split-sidebar")
    elif shell == "stack":
        classes.append("ourui-shell-stack")
    elif shell == "row":
        classes.append("ourui-shell-row")
    elif shell == "grid":
        classes.append("ourui-grid")
    for key, prefix in (("gap", "ourui-gap"), ("pad", "ourui-pad"), ("align", "ourui-align"), ("justify", "ourui-justify")):
        val = attrs.get(key)
        if isinstance(val, str) and val:
            classes.append(f"{prefix}-{val}")
    motion = attrs.get("motion")
    if isinstance(motion, str) and motion and motion != "none":
        classes.append(f"ourui-motion-{motion}")
    return classes


def _classes_for(node: dict[str, Any]) -> list[str]:
    attrs = node.get("attributes", {})
    layout = attrs.get("layout", "none")
    role = attrs.get("role", "")
    classes: list[str] = []
    if role not in {"nav", "footer"}:
        classes.extend(_layout_intent_classes(attrs))
        if not any(c.startswith("ourui-shell-") or c == "ourui-grid" for c in classes):
            if layout == "vertical":
                classes.append("ourui-col")
            elif layout == "horizontal":
                classes.append("ourui-row")
            elif layout == "grid":
                classes.append("ourui-grid")
    if role == "card":
        classes.append("ourui-card")
        if attrs.get("motion") in {"enter", "reveal", "press"}:
            classes.append(f"ourui-motion-{attrs['motion']}")
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
        if attrs.get("motion") == "press":
            classes.append("ourui-motion-press")
    if role == "theme-toggle":
        classes.append("ourui-theme-toggle")
        classes.append("ourui-control")
    if role == "copy-button":
        classes.append("ourui-copy-button")
        classes.append("ourui-control")
        tone = _tone_name(attrs)
        if tone:
            classes.append(f"ourui-tone-{tone}")
    if role == "input":
        classes.append("ourui-input")
        if attrs.get("type") == "textarea":
            classes.append("ourui-textarea")
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
    if role == "footer":
        classes.append("ourui-footer")
    if role == "canvas":
        classes.append("ourui-canvas")
    if role == "frame":
        classes.append("ourui-frame")
    if role == "image":
        classes.append("ourui-image")
        fit = attrs.get("fit") or "cover"
        classes.append(f"ourui-fit-{fit}")
    if role == "icon":
        classes.append("ourui-icon")
    if role == "code":
        classes.append("ourui-code")
    if role == "menu":
        classes.append("ourui-menu")
    if role == "section" and attrs.get("chrome") == "tabs":
        classes.append("ourui-playground-tabs")
    if role == "section" and attrs.get("chrome") == "file-tabs":
        classes.append("ourui-file-tab-row")
    if role == "text" and attrs.get("chrome") == "file-tab":
        classes.append("ourui-file-tab")
    if role == "text" and attrs.get("chrome") == "result-hero":
        classes.append("ourui-result-hero")
    if role in {"section", "hero", "shell", "page"} and attrs.get("motion") in {"enter", "reveal"}:
        classes.append(f"ourui-motion-{attrs['motion']}")
    if (
        node["kind"] == "Leaf"
        and "ourui-control" not in classes
        and "ourui-link" not in classes
        and "ourui-input" not in classes
        and "ourui-select" not in classes
        and "ourui-toggle" not in classes
        and "ourui-slider" not in classes
        and "ourui-nav" not in classes
        and "ourui-canvas" not in classes
        and "ourui-image" not in classes
        and "ourui-icon" not in classes
        and "ourui-code" not in classes
        and "ourui-theme-toggle" not in classes
        and "ourui-copy-button" not in classes
        and "ourui-menu" not in classes
        and "ourui-footer" not in classes
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


def _state_attrs(attrs: dict[str, Any]) -> str:
    parts: list[str] = []
    if attrs.get("disabled") in (True, "true", 1, "1"):
        parts.append(" disabled")
        parts.append(' aria-disabled="true"')
    if attrs.get("invalid") in (True, "true", 1, "1"):
        parts.append(' aria-invalid="true"')
    if attrs.get("loading") in (True, "true", 1, "1"):
        parts.append(' aria-busy="true"')
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
    if input_type != "textarea":
        parts.append(f' type="{html.escape(str(input_type), quote=True)}"')
    placeholder = attrs.get("placeholder")
    if isinstance(placeholder, str) and placeholder:
        parts.append(f' placeholder="{html.escape(placeholder, quote=True)}"')
    value = attrs.get("value")
    if input_type != "textarea" and value is not None and not isinstance(value, dict):
        parts.append(f' value="{html.escape(str(value), quote=True)}"')
    return "".join(parts) + _state_attrs(attrs)


def _textarea_body(attrs: dict[str, Any]) -> str:
    value = attrs.get("value")
    if value is None or isinstance(value, dict):
        return ""
    return html.escape(str(value))


def _frame_attrs(attrs: dict[str, Any]) -> str:
    parts: list[str] = []
    title = attrs.get("title") or "Result"
    parts.append(f' title="{html.escape(str(title), quote=True)}"')
    parts.append(' sandbox="allow-scripts allow-forms allow-same-origin"')
    srcdoc = attrs.get("srcdoc")
    if srcdoc is not None and not isinstance(srcdoc, dict):
        parts.append(f' srcdoc="{html.escape(str(srcdoc), quote=True)}"')
    bind = attrs.get("bind")
    if isinstance(bind, str) and bind:
        parts.append(f' data-ourui-bind="{html.escape(bind, quote=True)}"')
    return "".join(parts) + _state_attrs(attrs)


def _select_attrs(attrs: dict[str, Any]) -> str:
    return "".join(_field_name_attrs(attrs)) + _state_attrs(attrs)


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
    return "".join(parts) + _state_attrs(attrs)


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
    return "".join(parts) + _state_attrs(attrs)


def _wrap_field(pad: str, label: Any, control_lines: list[str], *, row: bool = False) -> list[str]:
    if not isinstance(label, str) or not label:
        return [f"{pad}{line}" if not line.startswith(pad) else line for line in control_lines]
    lab = html.escape(label)
    cls = "ourui-toggle-row" if row else "ourui-field"
    if row:
        inner = [f"{pad}  {control_lines[0].lstrip()}", f'{pad}  <span class="ourui-field-label">{lab}</span>']
        return [f'{pad}<label class="{cls}">', *inner, f"{pad}</label>"]
    return [
        f'{pad}<label class="{cls}">',
        f'{pad}  <span class="ourui-field-label">{lab}</span>',
        *[f"{pad}  {line.lstrip()}" if line.strip().startswith("<") else line for line in control_lines],
        f"{pad}</label>",
    ]


# Minimal Reicon-style path set (inline SVG host — names match common icon ids)
_ICON_PATHS: dict[str, str] = {
    "sun": "M12 4V2M12 22v-2M4.93 4.93 3.51 3.51M20.49 20.49l-1.42-1.42M4 12H2M22 12h-2M4.93 19.07 3.51 20.49M20.49 3.51l-1.42 1.42M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
    "moon": "M21 14.5A8.5 8.5 0 1 1 9.5 3 7 7 0 0 0 21 14.5z",
    "menu": "M4 7h16M4 12h16M4 17h16",
    "copy": "M8 8h10v12H8zM6 16H4V4h12v2",
    "check": "M5 12l5 5L20 7",
    "image": "M4 5h16v14H4zM8 11l3 3 5-5",
    "code": "M8 8l-4 4 4 4M16 8l4 4-4 4",
}


def _icon_svg(name: str) -> str:
    path = _ICON_PATHS.get(name, _ICON_PATHS["menu"])
    return (
        f'<svg viewBox="0 0 24 24" aria-hidden="true" data-reicon="{html.escape(name)}">'
        f'<path d="{path}" fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


def _collect_meta(nodes: dict[str, dict[str, Any]], roots: list[str] | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if roots:
        stack = list(roots)
        seen: set[str] = set()
        walk: list[str] = []
        while stack:
            nid = stack.pop()
            if nid in seen or nid not in nodes:
                continue
            seen.add(nid)
            walk.append(nid)
            stack.extend(reversed(nodes[nid].get("children") or []))
        candidates = walk
    else:
        candidates = list(nodes)
    for nid in candidates:
        node = nodes[nid]
        if node.get("attributes", {}).get("role") != "meta":
            continue
        attrs = node.get("attributes", {})
        if isinstance(attrs.get("title"), str):
            out["title"] = attrs["title"]
        if isinstance(attrs.get("description"), str):
            out["description"] = attrs["description"]
        og = attrs.get("og")
        if isinstance(og, dict):
            out["og"] = og
    return out


def _render_slot_block(
    pad: str,
    title: str,
    ids: list[str],
    nodes: dict[str, dict[str, Any]],
    indent: int,
) -> list[str]:
    if not ids:
        return []
    out = [f'{pad}  <div class="ourui-{title}">']
    for cid in ids:
        if cid in nodes:
            out.extend(_render_node(cid, nodes, indent + 2))
    out.append(f"{pad}  </div>")
    return out


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

    if role == "meta":
        return []  # head-only

    if role == "input":
        field = _input_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        if node_attrs.get("type") == "textarea":
            body = _textarea_body(node_attrs)
            return _wrap_field(
                pad,
                node_attrs.get("label"),
                [f"<textarea{attrs}>{body}</textarea>"],
            )
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
        return [f"{pad}<select{attrs}>", *opt_lines, f"{pad}</select>"]

    if role == "toggle":
        field = _toggle_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        return _wrap_field(pad, node_attrs.get("label"), [f"<input{attrs} />"], row=True)

    if role == "slider":
        field = _slider_attrs(node_attrs)
        attrs = f"{class_attr}{data_role}{data_id}{field}{events}"
        return _wrap_field(pad, node_attrs.get("label"), [f"<input{attrs} />"])

    if role == "theme-toggle":
        attrs = f'{class_attr}{data_role}{data_id} type="button" data-ourui-theme-toggle="1" aria-label="Toggle color theme"'
        children = node.get("children", [])
        if children:
            lines = [f"{pad}<button{attrs}>"]
            for child_id in children:
                if child_id in nodes:
                    lines.extend(_render_node(child_id, nodes, indent + 1))
            lines.append(f"{pad}</button>")
            return lines
        label = html.escape(str(node_attrs.get("text") or "Theme"))
        return [f"{pad}<button{attrs}>{label}</button>"]

    if role == "copy-button":
        label = html.escape(str(node_attrs.get("text") or "Copy"))
        copy_val = node_attrs.get("copy") or node_attrs.get("value") or ""
        copy_attr = f' data-ourui-copy="{html.escape(str(copy_val), quote=True)}"'
        attrs = f'{class_attr}{data_role}{data_id} type="button"{copy_attr}{_state_attrs(node_attrs)}{events}'
        return [f"{pad}<button{attrs}>{label}</button>"]

    if role == "canvas":
        mode = node_attrs.get("mode") or "gradient"
        rm = node_attrs.get("reduced_motion") or "static"
        cfg = node_attrs.get("config") if isinstance(node_attrs.get("config"), dict) else {}
        payload = {"mode": mode, "reduced_motion": rm, **cfg}
        cfg_json = html.escape(json.dumps(payload, separators=(",", ":")), quote=True)
        attrs = (
            f'{class_attr}{data_role}{data_id} data-ourui-canvas="1" '
            f'data-ourui-canvas-config="{cfg_json}"'
        )
        return [f"{pad}<canvas{attrs}></canvas>"]

    if role == "frame":
        attrs = f"{class_attr}{data_role}{data_id}{_frame_attrs(node_attrs)}"
        return [f"{pad}<iframe{attrs}></iframe>"]

    if role == "image":
        src = node_attrs.get("src") or ""
        alt = node_attrs.get("alt") or ""
        attrs = (
            f'{class_attr}{data_role}{data_id} src="{html.escape(str(src), quote=True)}" '
            f'alt="{html.escape(str(alt), quote=True)}"'
        )
        return [f"{pad}<img{attrs} />"]

    if role == "icon":
        name = str(node_attrs.get("name") or node_attrs.get("icon") or "menu")
        attrs = f'{class_attr}{data_role}{data_id} role="img" aria-label="{html.escape(name)}"'
        return [f"{pad}<span{attrs}>{_icon_svg(name)}</span>"]

    if role == "code":
        text = node_attrs.get("text") or node_attrs.get("value") or ""
        lang = node_attrs.get("language") or ""
        lang_attr = f' data-language="{html.escape(str(lang))}"' if lang else ""
        bind = node_attrs.get("bind")
        bind_attr = f' data-ourui-bind="{html.escape(str(bind))}"' if bind else ""
        attrs = f"{class_attr}{data_role}{data_id}{lang_attr}{bind_attr}"
        return [f"{pad}<pre{attrs}><code>{html.escape(str(text))}</code></pre>"]

    if role == "menu":
        items = node_attrs.get("items") if isinstance(node_attrs.get("items"), list) else []
        label = html.escape(str(node_attrs.get("text") or node_attrs.get("title") or "Menu"))
        attrs = f'{class_attr}{data_role}{data_id} data-ourui-menu="1"'
        lines = [
            f"{pad}<div{attrs}>",
            f'{pad}  <button type="button" class="ourui-control" data-ourui-menu-toggle="1">{label}</button>',
            f'{pad}  <div class="ourui-menu-panel">',
        ]
        for cid in items:
            if cid in nodes:
                lines.extend(_render_node(cid, nodes, indent + 2))
        lines.append(f"{pad}  </div>")
        lines.append(f"{pad}</div>")
        return lines

    if role == "nav":
        menu = node_attrs.get("menu") or "none"
        menu_attr = f' data-menu="{html.escape(str(menu))}"'
        attrs = f"{class_attr}{data_role}{data_id}{menu_attr}{events}"
        brand = node_attrs.get("brand")
        items = node_attrs.get("items") if isinstance(node_attrs.get("items"), list) else []
        actions = node_attrs.get("actions") if isinstance(node_attrs.get("actions"), list) else []
        slotted = set()
        if isinstance(brand, str):
            slotted.add(brand)
        slotted.update(i for i in items if isinstance(i, str))
        slotted.update(a for a in actions if isinstance(a, str))

        lines = [f"{pad}<nav{attrs}>"]
        if menu == "drawer":
            lines.append(
                f'{pad}  <button type="button" class="ourui-nav-menu-btn ourui-control" '
                f'data-ourui-drawer-open="1" aria-label="Open menu">{_icon_svg("menu")}</button>'
            )
        if isinstance(brand, str) and brand in nodes:
            lines.append(f'{pad}  <div class="ourui-nav-brand">')
            lines.extend(_render_node(brand, nodes, indent + 2))
            lines.append(f"{pad}  </div>")
        lines.extend(
            _render_slot_block(pad, "nav-items", [i for i in items if isinstance(i, str)], nodes, indent)
        )
        # fix class name: ourui-nav-items not ourui-nav-nav-items
        lines = [ln.replace("ourui-nav-nav-items", "ourui-nav-items") for ln in lines]
        lines.extend(
            _render_slot_block(pad, "nav-actions", [a for a in actions if isinstance(a, str)], nodes, indent)
        )
        lines = [ln.replace("ourui-nav-nav-actions", "ourui-nav-actions") for ln in lines]
        for child_id in node.get("children", []):
            if child_id in slotted or child_id not in nodes:
                continue
            lines.extend(_render_node(child_id, nodes, indent + 1))
        lines.append(f"{pad}</nav>")
        if menu == "drawer":
            lines.append(f'{pad}<div class="ourui-nav-drawer" data-ourui-drawer="1" hidden>')
            lines.append(f'{pad}  <div class="ourui-nav-drawer-panel">')
            lines.append(
                f'{pad}    <button type="button" class="ourui-control" data-ourui-drawer-close="1">Close</button>'
            )
            for cid in items:
                if isinstance(cid, str) and cid in nodes:
                    lines.extend(_render_node(cid, nodes, indent + 2))
            lines.append(f"{pad}  </div>")
            lines.append(f"{pad}</div>")
        return lines

    if role == "footer":
        attrs = f"{class_attr}{data_role}{data_id}{events}"
        brand = node_attrs.get("brand")
        links = node_attrs.get("links") if isinstance(node_attrs.get("links"), list) else []
        meta = node_attrs.get("meta") if isinstance(node_attrs.get("meta"), list) else []
        slotted: set[str] = set()
        if isinstance(brand, str):
            slotted.add(brand)
        slotted.update(i for i in links if isinstance(i, str))
        slotted.update(m for m in meta if isinstance(m, str))
        lines = [f"{pad}<footer{attrs}>"]
        if isinstance(brand, str) and brand in nodes:
            lines.append(f'{pad}  <div class="ourui-footer-brand">')
            lines.extend(_render_node(brand, nodes, indent + 2))
            lines.append(f"{pad}  </div>")
        lines.extend(_render_slot_block(pad, "footer-links", [i for i in links if isinstance(i, str)], nodes, indent))
        lines = [ln.replace("ourui-footer-footer-links", "ourui-footer-links") for ln in lines]
        lines.extend(_render_slot_block(pad, "footer-meta", [m for m in meta if isinstance(m, str)], nodes, indent))
        lines = [ln.replace("ourui-footer-footer-meta", "ourui-footer-meta") for ln in lines]
        for child_id in node.get("children", []):
            if child_id in slotted or child_id not in nodes:
                continue
            lines.extend(_render_node(child_id, nodes, indent + 1))
        lines.append(f"{pad}</footer>")
        return lines

    children = node.get("children", [])
    state = _state_attrs(node_attrs) if role == "button" else ""
    attrs = f"{class_attr}{data_role}{data_id}{link}{events}{state}"

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
        role = node.get("attributes", {}).get("role")
        # Also update canvas/code binds via sibling attrs if needed — Text only here
        _ = role
# Also update form/control value binds + Code text from State
    for node in out["nodes"].values():
        attrs = node.get("attributes", {}) or {}
        bind = attrs.get("bind")
        if bind in state_values and attrs.get("role") in {"input", "select", "toggle", "slider", "code", "frame"}:
            attrs["value"] = state_values[bind]
            if attrs.get("role") == "code":
                attrs["text"] = state_values[bind]
            if attrs.get("role") == "frame":
                attrs["srcdoc"] = state_values[bind]
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
    meta = _collect_meta(nodes, roots)
    doc_title = meta.get("title") or title
    body_lines: list[str] = ['  <div class="ourui-root">']
    for root in roots:
        body_lines.extend(_render_node(root, nodes, 2))
    body_lines.append("  </div>")

    js = emit_js(rtr, hmr=hmr).rstrip("\n")
    css = emit_css(resolved_design=resolved_design).rstrip("\n")
    head_extra: list[str] = []
    desc = meta.get("description")
    if isinstance(desc, str) and desc:
        head_extra.append(f'  <meta name="description" content="{html.escape(desc, quote=True)}" />')
    og = meta.get("og")
    if isinstance(og, dict):
        for key, val in og.items():
            if val is None:
                continue
            prop = f"og:{key}" if not str(key).startswith("og:") else str(key)
            head_extra.append(
                f'  <meta property="{html.escape(prop, quote=True)}" content="{html.escape(str(val), quote=True)}" />'
            )
    # Google Fonts for token fonts (display + sans)
    head_extra.append(
        '  <link rel="preconnect" href="https://fonts.googleapis.com" />'
    )
    head_extra.append(
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />'
    )
    head_extra.append(
        '  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600&family=Fraunces:opsz,wght@9..144,600&display=swap" rel="stylesheet" />'
    )

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8" />',
        '  <meta name="viewport" content="width=device-width, initial-scale=1" />',
        f"  <title>{html.escape(str(doc_title))}</title>",
        *head_extra,
        "  <style>",
        css,
        "  </style>",
        "</head>",
        "<body>",
        *body_lines,
        "  <script>",
        _PLASMA_ENGINE.rstrip("\n"),
        "  </script>",
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
