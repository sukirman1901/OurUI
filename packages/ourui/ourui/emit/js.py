from __future__ import annotations

import json
from typing import Any

RPC_PATH = "/__ourui/call/"


def emit_js(rtr: dict[str, Any]) -> str:
    """Runtime shim: RPC for @server + DOM bind updates for State."""
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
  function applyState(state) {{
    if (!state) return;
    Object.keys(state).forEach((name) => {{
      document.querySelectorAll('[data-ourui-bind="' + name + '"]').forEach((el) => {{
        el.textContent = String(state[name]);
      }});
    }});
  }}
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
      if (data && data.state) applyState(data.state);
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
  window.OurUI = {{ invoke, handlers, applyState }};
}})();
"""
