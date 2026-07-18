# ADR-006: Chrome intents — Nav, placement, not raw CSS `position`

**Status:** Accepted + Implemented (Phase **S3a**, package `0.3.3`; drawer/`menu=` in **S6** / `0.4.0`)  
**Date:** 2026-07-18  
**Relates:** [ADR-005](ADR-005-intent-emit-escape.md)

## Context

Emit CSS today is a thin base (flex column/row/grid + tokens). Product UIs (Plasma landing, SaaS shells) need **fixed / sticky / absolute** chrome. Authors asked: if styling is to approach usable quality, these must be **definable** — and `ui.Nav` must be a real product control, not a bare `<nav>` with browser defaults.

Exposing `position="fixed"` / every CSS layout property as Stable authoring repeats usePyX and rejects ADR-005.

## Decision

### 1. Placement is an **intent enum**, not a CSS dump

HostNode may carry `placement` (semantic). **Emitter** maps to CSS `position` + insets + z-index.

| Author intent `placement=` | Typical emit |
|----------------------------|--------------|
| `flow` (default) | `position: static` (document flow) |
| `sticky-top` | `position: sticky; top: 0; z-index: …` |
| `fixed-top` | `position: fixed; inset-inline: 0; top: 0; z-index: …` |
| `fixed-bottom` | `position: fixed; bottom: 0; …` |
| `overlay` | `position: absolute` within nearest `Shell` / positioned ancestor |
| `backdrop` | full-bleed absolute/fixed behind content (hero media layer) |

Authors **do not** write `static|fixed|absolute|relative|sticky` as free strings in P0/S Stable API.

### 2. `ui.Nav` is a **chrome component**, not “sekadar nav”

```python
ui.Nav(
    brand=ui.Link("Plasma", href="/"),
    items=[
        ui.Link("Feature", href="#features"),
        ui.Link("Playground", href="#playground"),
        ui.Link("FAQ", href="#faq"),
    ],
    actions=[
        ui.Button("Theme", …),           # later: icon toggle
        ui.Link("Open Studio", href="/app"),
    ],
    placement="sticky-top",   # or fixed-top
    tone="glass",             # emit: translucent bg + blur token
)
```

Defaults (so OurUI looks intentional out of the box):

| Concern | Default |
|---------|---------|
| Placement | `sticky-top` on marketing; `fixed-top` in `ui.Shell` app chrome |
| Layout | brand \| items (center/start) \| actions — flex row, gap from tokens |
| Tone | `solid` (token surface) or `glass` (backdrop-filter + alpha) |
| Mobile | items collapse to menu intent later (`menu="drawer"`) — S6 |
| Active route | match `href` to current path when served |

Emit: `<nav class="ourui-nav ourui-nav-sticky-top ourui-tone-glass">…</nav>` with **authored CSS in the compiler**, not empty browser defaults.

### 3. Where placement is allowed (whitelist)

| Kind | `placement=` |
|------|----------------|
| `Nav` | yes (primary) |
| `Shell` | optional `chrome=` / child Nav |
| `Hero` | `backdrop` for media layer (with Canvas later) |
| `Page` / `Section` / `Card` | no free `position` — use Shell/Nav/overlay slots |

### 4. Layout intents stay semantic (ADR-005 S4)

`layout=stack|row|split-3|grid` + future `gap=` / `pad=` / `align=` — still **not** `justify-content` / `float` / `z-index` as author API. Z-index lives inside placement presets (nav above content, backdrop below).

## Non-goals

- `ui.div(position="absolute", top=4, z=50)`
- Full CSS position/flex/grid encyclopedia as Python kwargs
- Pixel-perfect Plasma without **S5 Canvas** (placement alone ≠ living background)

## Implementation order

1. **S3a** — `ui.Nav` + `placement` + `tone=solid|glass` — **Done** (`0.3.3`)
2. **S3** — type / space / elevation tokens — **Done** (`0.4.0`)
3. **S4** — richer layout on Shell/Section — **Done** (`0.4.0`)
4. **S5–S6** — Canvas backdrop, drawer menu, theme toggle — **Done** (`0.4.0`)

## Consequences

- CSS `position` **is** defined — inside the **emitter tables**, driven by `placement`.
- `ui.Nav` ships with **defaults people would actually use** (sticky glass/solid bar), not an unstyled tag.
- Dump schema bumped when `placement` / `tone` / `menu` appear on HostNode (schema **15** → **21**).
- Demo landing uses `ui.Nav` + drawer + ThemeToggle.
