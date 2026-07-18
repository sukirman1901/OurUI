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
| **Lower** | UI intent is lowered into render-ready trees (layout and host nodes). |
| **Emit** | The browser receives HTML, embedded CSS, and JS for RPC and live updates. |

You never write HTML, CSS, or JavaScript by hand for app logic. The CLI exposes each step:

```bash
ourui dump app.py    # inspect compiler artifacts (JSON)
ourui emit app.py    # static HTML snapshot
ourui serve app.py   # full interactive server
```

## What you write vs what the browser gets

**You write:** Python — `ui.Page`, `Hero`, `State`, `@server` functions, `ui.Theme`, and `route=` for multiple pages.

**The browser gets:** A complete document with `--ourui-*` CSS variables, markup for your components, and a shim that calls your Python handlers over HTTP when users click buttons or submit actions.

Static `emit` is useful for previews and debugging; interactive apps need `ourui serve` so `@server` handlers run on the server.

## Going deeper

This page stays at the user mental model — no IR names or graph internals.

Contributors and compiler hackers should read the **[Compiler Book](../../../COMPILER_BOOK.md)** for parse/analyze/lower details, artifact formats, and phase history.
