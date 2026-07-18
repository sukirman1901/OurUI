# How OurUI compiles

OurUI turns Python UI code into something a browser can run. You describe **intent** — pages, components, state, and server handlers — and the compiler produces **implementation**: HTML structure, CSS (including design tokens), and a small JavaScript shim for interactivity.

## The pipeline (mental model)

```text
Parse → Analyze → Lower → Emit
```

| Stage | What happens (user view) |
|-------|---------------------------|
| **Parse** | Your `.py` module is read as Python source. OurUI finds `ui.Page`, components, `State`, and `@server` handlers. |
| **Analyze** | The compiler checks structure, routes, theme usage, and handler bindings. |
| **Lower** | Intent becomes render-ready trees; a Presentation Graph + Design System yield **Resolved Design**. |
| **Emit** | The browser receives HTML, CSS, and JS. Emit **requires** Resolved Design (Host Contract). |

You never write HTML, CSS, or JavaScript by hand for app logic. The CLI exposes each step:

```bash
ourui dump app.py    # inspect compiler artifacts (JSON)
ourui emit app.py    # static HTML snapshot
ourui serve app.py   # full interactive server
```

## What you write vs what the browser gets

**You write:** Python — `ui.Page`, `Hero`, `Nav`, `Canvas`, `State`, `@server`, `ui.Theme`, `route=`.

**The browser gets:** A complete document with `--ourui-*` CSS variables (color, type, space, elevation), markup for your components, optional WebGL canvas, and a shim that calls your Python handlers over HTTP.

Static `emit` is useful for previews; interactive apps need `ourui serve`.

## Going deeper

This page stays at the user mental model.

Contributors: **[Compiler Book](../../../COMPILER_BOOK.md)**, [ARCHITECTURE.md](../../../ARCHITECTURE.md), [VISION.md](../../../VISION.md).
