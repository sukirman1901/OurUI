from __future__ import annotations

import json
from typing import Any

RPC_PATH = "/__ourui/call/"


def emit_js(rtr: dict[str, Any]) -> str:
    """Minimal OurUI runtime shim. Server handlers POST to /__ourui/call/<name>."""
    handlers = rtr.get("handlers", {})
    table = {
        name: {"kind": meta.get("kind", "client")}
        for name, meta in sorted(handlers.items())
    }
    table_json = json.dumps(table, separators=(",", ":"), sort_keys=True)
    rpc = json.dumps(RPC_PATH)
    return f"""\
(() => {{
  const handlers = {table_json};
  const rpcBase = {rpc};
  async function invoke(name, payload) {{
    const meta = handlers[name] || {{ kind: "client" }};
    const detail = {{ handler: name, kind: meta.kind }};
    window.dispatchEvent(new CustomEvent("ourui:call", {{ detail }}));
    if (meta.kind === "server") {{
      const res = await fetch(rpcBase + encodeURIComponent(name), {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify(payload || {{}}),
      }});
      const data = await res.json();
      window.dispatchEvent(new CustomEvent("ourui:result", {{ detail: data }}));
      if (!res.ok || !data.ok) {{
        console.error("[ourui] server call failed:", name, data);
        return data;
      }}
      console.info("[ourui] server call ok:", name, data.result);
      return data;
    }}
    console.info("[ourui] client call:", name);
    return {{ ok: true, handler: name, kind: "client" }};
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
