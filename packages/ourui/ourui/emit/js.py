from __future__ import annotations

import json
from typing import Any


def emit_js(rtr: dict[str, Any]) -> str:
    """Minimal OurUI runtime shim (<~1KB). Consumes RTR handlers + data-ourui-on-* only."""
    handlers = rtr.get("handlers", {})
    # Deterministic JSON embed
    table = {
        name: {"kind": meta.get("kind", "client")}
        for name, meta in sorted(handlers.items())
    }
    table_json = json.dumps(table, separators=(",", ":"), sort_keys=True)
    return f"""\
(() => {{
  const handlers = {table_json};
  function invoke(name) {{
    const meta = handlers[name] || {{ kind: "client" }};
    const detail = {{ handler: name, kind: meta.kind }};
    window.dispatchEvent(new CustomEvent("ourui:call", {{ detail }}));
    if (meta.kind === "server") {{
      console.info("[ourui] server call (stub):", name);
    }} else {{
      console.info("[ourui] client call:", name);
    }}
  }}
  document.addEventListener("click", (ev) => {{
    const el = ev.target && ev.target.closest && ev.target.closest("[data-ourui-on-click]");
    if (!el) return;
    ev.preventDefault();
    invoke(el.getAttribute("data-ourui-on-click"));
  }});
  window.OurUI = {{ invoke, handlers }};
}})();
"""
