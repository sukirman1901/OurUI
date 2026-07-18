# How OurUI compiles

OurUI turns Python UI code into something a browser can run. You describe **intent** — pages, thin components, state, server handlers, and **style utilities** (`aspect=`, `pad_x=`, …) — and the compiler produces **implementation**: HTML, CSS (theme roles + finite `.ourui-*` utilities), and a small JavaScript shim for interactivity.

Same *compile idea* as Tailwind; authoring is Python props, not class strings.

## The pipeline (mental model)

```text
Parse → Analyze → Lower → Emit
```

| Stage | What happens (user view) |
|-------|---------------------------|
| **Parse** | Your `.py` module is read as Python source. OurUI finds `ui.Page`, components, `State`, and `@server` handlers. |
| **Analyze** | The compiler checks structure, routes, theme usage, and handler bindings. |
| **Lower** | Intent becomes render-ready trees; Presentation Graph + theme defaults/overrides yield **Resolved Design** (roles + scales). |
| **Emit** | The browser receives HTML, CSS, and JS. Emit **requires** Resolved Design (Host Contract). |

You never write HTML, CSS, or JavaScript by hand for app logic. The CLI exposes each step:

```bash
ourui dump app.py    # inspect compiler artifacts (JSON)
ourui emit app.py    # static HTML snapshot
ourui serve app.py   # full interactive server
```

## What you write vs what the browser gets

**You write:** Python — `ui.Page`, layout kinds, `aspect=` / `gap=` / …, `State`, `@server`, `ui.Theme`, `route=`.

**The browser gets:** A document with `--ourui-*` CSS variables, emitted utility classes for style intents, markup for your primitives, optional WebGL canvas, and a shim that calls your Python handlers over HTTP.

Static `emit` is useful for previews; interactive apps need `ourui serve`.

## Utilities vs theme

- **Utilities** (foundation): e.g. aspect-ratio → `aspect=` — see [Style intents](../reference/style-intents.md).
- **`ui.Theme`** (thin sheet): brand roles, density, page measure — see [Theme](../reference/theme.md).
- **Thin `ui.*` kinds**: emit mapping (`Page`, `Nav`, `Button`, …) — not a component marketplace.

## Going deeper

This page stays at the user mental model.

Contributors: **[Compiler Book](../../../COMPILER_BOOK.md)**, [ARCHITECTURE.md](../../../ARCHITECTURE.md), [VISION.md](../../../VISION.md).
