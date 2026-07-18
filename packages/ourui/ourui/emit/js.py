from __future__ import annotations

import json
from typing import Any

RPC_PATH = "/__ourui/call/"
HMR_PATH = "/__ourui/hmr"


def emit_js(rtr: dict[str, Any], *, hmr: bool = False) -> str:
    """Runtime shim: RPC for @server + DOM bind updates; optional HMR EventSource."""
    handlers = rtr.get("handlers", {})
    table = {
        name: {"kind": meta.get("kind", "client")}
        for name, meta in sorted(handlers.items())
    }
    table_json = json.dumps(table, separators=(",", ":"), sort_keys=True)
    rpc = json.dumps(RPC_PATH)
    hmr_path = json.dumps(HMR_PATH)
    hmr_block = ""
    if hmr:
        hmr_block = f"""
  try {{
    const es = new EventSource({hmr_path});
    es.addEventListener("reload", () => location.reload());
  }} catch (err) {{
    console.warn("[ourui] HMR unavailable", err);
  }}
"""
    return f"""\
(() => {{
  const handlers = {table_json};
  const rpcBase = {rpc};
  function applyState(state) {{
    if (!state) return;
    Object.keys(state).forEach((name) => {{
      document.querySelectorAll('[data-ourui-bind="' + name + '"]').forEach((el) => {{
        const tag = (el.tagName || "").toLowerCase();
        const next = String(state[name]);
        if (tag === "input" || tag === "textarea" || tag === "select") {{
          el.value = next;
        }} else {{
          el.textContent = next;
        }}
      }});
    }});
  }}
  function collectFields(scope) {{
    const root = scope || document;
    const payload = {{}};
    root.querySelectorAll("[data-ourui-field]").forEach((el) => {{
      const key = el.getAttribute("data-ourui-field");
      if (!key) return;
      payload[key] = el.value;
    }});
    return payload;
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
    invoke(el.getAttribute("data-ourui-on-click"), collectFields());
  }});
  window.OurUI = {{ invoke, handlers, applyState, collectFields }};{hmr_block}
}})();
"""
