# HTML emitter

**Status:** Draft (Phase E — `ourui emit`).

Maps **HostNode** → HTML. Must not read Python AST or IIR ([I1](../../INVARIANTS.md), [I2](../../INVARIANTS.md)).

Event bindings from RTR `attributes.events.click` become `data-ourui-on-click`. The HTML document inlines the JS shim from [spec/runtime/overview.md](../runtime/overview.md).

| HostNode / role | HTML |
|---|---|
| `Container` + layout | `<div class="ourui-col|row|grid">` |
| `role=page` | `<main>` |
| `role=hero` | `<header>` |
| `role=section` | `<section>` |
| `role=button` | `<button class="ourui-control">` |
| `role=card` | `<div class="ourui-card">` |
| `Text` | `<span data-slot="…">` |

CSS is inlined in the HTML document for P0–E; `emit_bundle` also returns separate `css`. JS is empty until interactivity lands.

## CLI

```bash
ourui emit examples/example.py
ourui emit examples/example.py -o out.html --title "Welcome"
```

Implementation: `packages/ourui/ourui/emit/html.py`.
