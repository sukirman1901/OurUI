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
  function csrfToken() {{
    const m = document.querySelector('meta[name="ourui-csrf"]');
    return m ? (m.getAttribute("content") || "") : "";
  }}
  function applyState(state) {{
    if (!state) return;
    Object.keys(state).forEach((name) => {{
      document.querySelectorAll('[data-ourui-bind="' + name + '"]').forEach((el) => {{
        const tag = (el.tagName || "").toLowerCase();
        const role = el.getAttribute("data-role") || "";
        const next = state[name];
        if (tag === "iframe") {{
          el.srcdoc = next == null ? "" : String(next);
        }} else if (role === "dialog" || role === "toast") {{
          const on = Boolean(next) && next !== "false" && next !== "0" && next !== "";
          el.setAttribute("data-open", on ? "true" : "false");
        }} else if (role === "show" || role === "when") {{
          const on = Boolean(next) && next !== "false" && next !== "0" && next !== "";
          el.setAttribute("data-show", on ? "true" : "false");
        }} else if (role === "list" && Array.isArray(next)) {{
          el.innerHTML = "";
          next.forEach((item) => {{
            const li = document.createElement("li");
            li.className = "ourui-list-item";
            if (item && typeof item === "object") {{
              li.textContent = String(item.label || item.text || item.name || JSON.stringify(item));
            }} else {{
              li.textContent = item == null ? "" : String(item);
            }}
            el.appendChild(li);
          }});
        }} else if (role === "table" && Array.isArray(next)) {{
          let columns = [];
          try {{ columns = JSON.parse(el.getAttribute("data-ourui-columns") || "[]"); }} catch (e) {{}}
          let tbody = el.querySelector("tbody");
          if (!tbody) {{
            tbody = document.createElement("tbody");
            el.appendChild(tbody);
          }}
          tbody.innerHTML = "";
          next.forEach((row) => {{
            const tr = document.createElement("tr");
            if (row && typeof row === "object" && !Array.isArray(row)) {{
              (columns.length ? columns : Object.keys(row)).forEach((col) => {{
                const td = document.createElement("td");
                td.textContent = row[col] == null ? "" : String(row[col]);
                tr.appendChild(td);
              }});
            }} else if (Array.isArray(row)) {{
              row.forEach((cell) => {{
                const td = document.createElement("td");
                td.textContent = cell == null ? "" : String(cell);
                tr.appendChild(td);
              }});
            }} else {{
              const td = document.createElement("td");
              td.textContent = row == null ? "" : String(row);
              tr.appendChild(td);
            }}
            tbody.appendChild(tr);
          }});
        }} else if (tag === "input" && el.type === "checkbox") {{
          el.checked = Boolean(next) && next !== "false" && next !== "0" && next !== "";
        }} else if (tag === "input" || tag === "textarea" || tag === "select") {{
          el.value = next == null ? "" : String(next);
        }} else if (tag === "pre") {{
          const code = el.querySelector("code");
          const text = next == null ? "" : String(next);
          if (code) code.textContent = text;
          else el.textContent = text;
        }} else {{
          el.textContent = next == null ? "" : String(next);
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
      const body = Object.assign({{}}, payload || {{}});
      const csrf = csrfToken();
      if (csrf) body._csrf = csrf;
      const headers = {{ "Content-Type": "application/json" }};
      if (csrf) headers["X-OurUI-CSRF"] = csrf;
      const res = await fetch(rpcBase + encodeURIComponent(name), {{
        method: "POST",
        headers,
        body: JSON.stringify(body),
        credentials: "same-origin",
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
  document.addEventListener("submit", (ev) => {{
    const form = ev.target && ev.target.closest ? ev.target.closest("[data-ourui-on-submit]") : null;
    if (!form) return;
    ev.preventDefault();
    invoke(form.getAttribute("data-ourui-on-submit"), collectFields(form));
  }});
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
    const dialogClose = t.closest("[data-ourui-dialog-close]");
    if (dialogClose) {{
      ev.preventDefault();
      const dialog = dialogClose.closest('[data-role="dialog"]');
      if (dialog) dialog.setAttribute("data-open", "false");
      return;
    }}
    const el = t.closest("[data-ourui-on-click]");
    if (!el) return;
    ev.preventDefault();
    invoke(el.getAttribute("data-ourui-on-click"), collectFields());
  }});
  function initMotion() {{
    const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function splitText(el, mode) {{
      const flag = mode === "char" ? "data-ourui-chars" : "data-ourui-words";
      if (el.getAttribute(flag) === "1") return;
      const text = el.textContent || "";
      if (!text.trim()) return;
      el.setAttribute(flag, "1");
      if (reduce) return;
      el.textContent = "";
      let i = 0;
      if (mode === "char") {{
        Array.from(text).forEach((ch) => {{
          if (ch === " ") {{ el.appendChild(document.createTextNode(" ")); return; }}
          const span = document.createElement("span");
          span.className = "ourui-motion-char";
          span.textContent = ch;
          span.style.animationDelay = (i * 0.028) + "s";
          el.appendChild(span);
          i += 1;
        }});
        return;
      }}
      text.trim().split(/(\\s+)/).forEach((w) => {{
        if (/^\\s+$/.test(w)) {{ el.appendChild(document.createTextNode(w)); return; }}
        const span = document.createElement("span");
        span.className = "ourui-motion-word";
        span.textContent = w;
        span.style.animationDelay = (i * 0.045) + "s";
        el.appendChild(span);
        i += 1;
      }});
    }}
    function wrapMarquee(sel, vertical) {{
      document.querySelectorAll(sel).forEach((el) => {{
        if (el.getAttribute("data-ourui-marquee") === "1") return;
        el.setAttribute("data-ourui-marquee", "1");
        if (reduce) return;
        const kids = Array.from(el.children);
        if (kids.length) {{
          const track = document.createElement("div");
          track.className = "ourui-motion-marquee-track";
          kids.forEach((k) => track.appendChild(k));
          kids.forEach((k) => track.appendChild(k.cloneNode(true)));
          el.appendChild(track);
          return;
        }}
        const text = (el.textContent || "").trim();
        if (!text) return;
        el.textContent = "";
        const track = document.createElement("span");
        track.className = "ourui-motion-marquee-track";
        track.textContent = text + " \\u00a0\\u00a0 " + text;
        el.appendChild(track);
      }});
    }}
    function stagger(sel) {{
      document.querySelectorAll(sel).forEach((el) => {{
        Array.from(el.children).forEach((child, idx) => child.style.setProperty("--ourui-stagger", String(idx)));
      }});
    }}
    function countUp(el) {{
      const raw = (el.getAttribute("data-ourui-count") || el.textContent || "").replace(/[^0-9.-]/g, "");
      const target = Number(raw);
      if (!Number.isFinite(target)) {{ el.setAttribute("data-ourui-inview", "true"); return; }}
      if (reduce) {{ el.textContent = String(target); el.setAttribute("data-ourui-inview", "true"); return; }}
      const start = performance.now();
      const dur = 900;
      const tick = (now) => {{
        const t = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = String(Math.round(target * eased));
        if (t < 1) requestAnimationFrame(tick);
        else el.setAttribute("data-ourui-inview", "true");
      }};
      requestAnimationFrame(tick);
    }}
    document.querySelectorAll('[data-ourui-motion="text.word-reveal"]').forEach((el) => splitText(el, "word"));
    document.querySelectorAll('[data-ourui-motion="text.char-reveal"]').forEach((el) => splitText(el, "char"));
    document.querySelectorAll('[data-ourui-motion="text.typewriter"]').forEach((el) => {{
      const len = (el.textContent || "").trim().length || 24;
      el.style.setProperty("--ourui-typewriter-steps", String(Math.max(8, len)));
      el.style.setProperty("--ourui-typewriter-ms", String(Math.min(2800, 40 * len)) + "ms");
    }});
    document.querySelectorAll('[data-ourui-motion="text.rolling"]').forEach((el) => {{
      if (el.getAttribute("data-ourui-roll") === "1") return;
      el.setAttribute("data-ourui-roll", "1");
      const parts = (el.textContent || "").split("|").map((s) => s.trim()).filter(Boolean);
      if (parts.length < 2) return;
      el.textContent = "";
      const inner = document.createElement("span");
      inner.className = "ourui-motion-roll-inner";
      parts.concat(parts[0]).forEach((p) => {{
        const line = document.createElement("span");
        line.style.display = "block";
        line.textContent = p;
        inner.appendChild(line);
      }});
      el.appendChild(inner);
    }});
    wrapMarquee('[data-ourui-motion="text.marquee"]');
    wrapMarquee('[data-ourui-motion="flow.logo-marquee"]');
    wrapMarquee('[data-ourui-motion="flow.infinite-slider"]');
    wrapMarquee('[data-ourui-motion="flow.vertical-marquee"]', true);
    stagger('[data-ourui-motion="reveal.stagger-children"], [data-ourui-motion="hero.stagger-copy"], [data-ourui-motion="grid.bento-reveal"], [data-ourui-motion="grid.cascade"], [data-ourui-motion="stack.poster-burst"]');
    document.querySelectorAll('[data-ourui-motion="hover.tilt"], [data-ourui-motion="perspective.tilt-card"], [data-ourui-motion="hover.magnetic"]').forEach((el) => {{
      if (reduce) return;
      el.addEventListener("pointermove", (ev) => {{
        const r = el.getBoundingClientRect();
        const x = (ev.clientX - r.left) / r.width - 0.5;
        const y = (ev.clientY - r.top) / r.height - 0.5;
        const motion = el.getAttribute("data-ourui-motion") || "";
        if (motion.indexOf("magnetic") >= 0) {{
          el.style.transform = "translate(" + (x * 10) + "px," + (y * 10) + "px)";
        }} else {{
          el.style.transform = "rotateY(" + (x * 8) + "deg) rotateX(" + (-y * 8) + "deg)";
        }}
      }});
      el.addEventListener("pointerleave", () => {{ el.style.transform = ""; }});
    }});
    document.querySelectorAll('[data-ourui-motion="hero.mouse-parallax"], [data-ourui-motion="hero.parallax"]').forEach((el) => {{
      if (reduce) return;
      window.addEventListener("pointermove", (ev) => {{
        const x = (ev.clientX / window.innerWidth - 0.5) * 12;
        const y = (ev.clientY / window.innerHeight - 0.5) * 8;
        el.style.transform = "translate(" + x + "px," + y + "px)";
      }}, {{ passive: true }});
    }});
    const inviewSel = '[data-ourui-motion="scroll.fade-in-view"], [data-ourui-motion="scroll.zoom"], [data-ourui-motion="scroll.parallax-layer"], [data-ourui-motion="scroll.reveal-line"], [data-ourui-motion="scroll.counter"], [data-ourui-motion="text.count-up"]';
    const scrollEls = document.querySelectorAll(inviewSel);
    if (scrollEls.length) {{
      const activate = (el) => {{
        const motion = el.getAttribute("data-ourui-motion") || "";
        if (motion === "scroll.counter" || motion === "text.count-up") countUp(el);
        else el.setAttribute("data-ourui-inview", "true");
      }};
      if (reduce || !("IntersectionObserver" in window)) {{
        scrollEls.forEach(activate);
      }} else {{
        const io = new IntersectionObserver((entries) => {{
          entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
              activate(entry.target);
              io.unobserve(entry.target);
            }}
          }});
        }}, {{ threshold: 0.12, rootMargin: "0px 0px -8% 0px" }});
        scrollEls.forEach((el) => io.observe(el));
      }}
    }}
  }}
  initCanvases();
  initMotion();
  window.OurUI = {{ invoke, handlers, applyState, collectFields, toggleTheme, initCanvases, initMotion, csrfToken }};{hmr_block}
}})();
"""
