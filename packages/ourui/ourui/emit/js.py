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
        const next = state[name];
        if (tag === "input" && el.type === "checkbox") {{
          el.checked = Boolean(next) && next !== "false" && next !== "0" && next !== "";
        }} else if (tag === "input" || tag === "textarea" || tag === "select") {{
          el.value = String(next);
        }} else {{
          el.textContent = String(next);
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
      if (el.type === "checkbox") {{
        payload[key] = !!el.checked;
      }} else {{
        payload[key] = el.value;
      }}
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
  function toggleTheme() {{
    const root = document.documentElement;
    const on = root.classList.toggle("dark");
    try {{ localStorage.setItem("ourui-theme", on ? "dark" : "light"); }} catch (e) {{}}
  }}
  try {{
    const saved = localStorage.getItem("ourui-theme");
    if (saved === "dark") document.documentElement.classList.add("dark");
  }} catch (e) {{}}
  function initCanvases() {{
    if (!window.Plasma || !window.Plasma.init) return;
    document.querySelectorAll("[data-ourui-canvas]").forEach((el) => {{
      if (el.__ouruiPlasma) return;
      let cfg = {{}};
      try {{ cfg = JSON.parse(el.getAttribute("data-ourui-canvas-config") || "{{}}"); }} catch (e) {{}}
      el.__ouruiPlasma = window.Plasma.init(el, cfg);
    }});
  }}
  document.addEventListener("click", (ev) => {{
    const t = ev.target;
    if (!t || !t.closest) return;
    const themeBtn = t.closest("[data-ourui-theme-toggle]");
    if (themeBtn) {{
      ev.preventDefault();
      toggleTheme();
      return;
    }}
    const copyBtn = t.closest("[data-ourui-copy]");
    if (copyBtn) {{
      ev.preventDefault();
      const text = copyBtn.getAttribute("data-ourui-copy") || "";
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => {{
          copyBtn.setAttribute("data-copied", "true");
          setTimeout(() => copyBtn.removeAttribute("data-copied"), 1200);
        }}).catch(() => {{}});
      }}
      return;
    }}
    const menuToggle = t.closest("[data-ourui-menu-toggle]");
    if (menuToggle) {{
      ev.preventDefault();
      const menu = menuToggle.closest("[data-ourui-menu]");
      if (menu) menu.setAttribute("data-open", menu.getAttribute("data-open") === "true" ? "false" : "true");
      return;
    }}
    const drawerOpen = t.closest("[data-ourui-drawer-open]");
    if (drawerOpen) {{
      ev.preventDefault();
      const drawer = document.querySelector("[data-ourui-drawer]");
      if (drawer) {{
        drawer.hidden = false;
        drawer.setAttribute("data-open", "true");
      }}
      return;
    }}
    const drawerClose = t.closest("[data-ourui-drawer-close]");
    if (drawerClose) {{
      ev.preventDefault();
      const drawer = document.querySelector("[data-ourui-drawer]");
      if (drawer) {{
        drawer.hidden = true;
        drawer.setAttribute("data-open", "false");
      }}
      return;
    }}
    const el = t.closest("[data-ourui-on-click]");
    if (!el) return;
    ev.preventDefault();
    invoke(el.getAttribute("data-ourui-on-click"), collectFields());
  }});
  initCanvases();
  window.OurUI = {{ invoke, handlers, applyState, collectFields, toggleTheme, initCanvases }};{hmr_block}
}})();
"""
