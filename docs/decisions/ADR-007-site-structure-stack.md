# ADR-007: Site structure stack — beyond Nav

**Status:** Accepted + **Implemented** (Phase S stack through S6, package `0.4.0`)  
**Date:** 2026-07-18  
**Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-006](ADR-006-chrome-nav-placement.md)

## Context

S1 (`Link` / `Shell`) only unlocked clickable routes and a crude split. The Plasma-shaped demo still looks “broken product”: no real page anatomy, weak color/type hierarchy, no modern motion. A usable OurUI must cover **whole site structure**, not Nav alone — and must eventually support **dynamic, modern UI** (responsive regions, elevation, animation) via intent→emit, not raw CSS encyclopedias.

## Decision: four layers (all required for “not jelek”)

```text
1. STRUCTURE   landmarks & section jobs     ← anatomy of a page/app
2. CHROME      Nav / topbar / sidebar       ← ADR-006
3. PRESENTATION tokens, type, space, tone   ← color & density
4. MOTION      named families, not random   ← modern feel
(+ MEDIA/ESCAPE  Image, Canvas/WebGL)       ← Plasma-class
```

Shipping only (1) without (3)+(4) still looks bad — that is the current demo.  
Shipping only Nav without structure/tokens/motion also fails.

### Layer 1 — Structure intents (page anatomy)

Not “div soup”. Named regions with **one job** each (marketing stack + app shell):

| Intent | Job | Emit sketch |
|--------|-----|-------------|
| `ui.Page` | Document root | `<main>` / page wrapper + optional pad for fixed chrome |
| `ui.Nav` | Primary chrome | ADR-006 |
| `ui.Hero` | First viewport composition | full-bleed / contained; optional `backdrop` |
| `ui.Section` | One purpose block | landmark + spacing rhythm |
| `ui.Shell` | App workspace regions | `split-*` / sidebar+main |
| `ui.Footer` | End matter / links | `<footer>` + stack/row |
| `ui.Aside` | Secondary column | complementary landmark |
| Later | `Banner`, `Toast`, `Drawer`, `Modal` | overlays with `placement` |

Marketing default stack (author should express this, compiler styles it):

```text
Nav → Hero → (Logo/proof) → Features → Playground → Audience → FAQ → CTA → Footer
```

App default stack:

```text
Nav(top) + Shell(sidebar | main | aside) → Footer optional
```

### Layer 2 — Chrome

`placement` / `tone` on Nav (and future Drawer) — ADR-006.

### Layer 3 — Presentation (warna, type, space)

Extend `--ourui-*`:

- **Color** roles (already) + surfaces (elevated, glass, overlay)
- **Type** scale: `display` / `title` / `body` / `muted` (fonts via Theme later)
- **Space** scale: denser rhythm than two spacing tokens
- **Elevation** / radius / border as tones on Card/Section/Hero

Author: `tone=`, `density=`, `ui.Theme(font_display=…)` — not `text-4xl` / `p-8`.

### Layer 4 — Motion (modern / dinamis)

Named intents only (prefer-reduced-motion respected in emit):

| Intent | Use |
|--------|-----|
| `motion="enter"` | section fade/slide on view |
| `motion="press"` | button/link feedback |
| `motion="nav"` | sticky bar / drawer |
| Marketing | `reveal` / hero presence — budget 2–3 / viewport |

Compiler emits CSS/JS motion presets — authors do not write keyframes by default.

### Honesty bar

| Claim | Reality |
|-------|---------|
| “S1 = modern UI” | **False** — structure hooks only |
| “Nav alone = website” | **False** — need Footer/Hero/Section rhythm + tokens + motion |
| “100% = all CSS properties” | **False** — 100% of **product intents** we choose to support |
| Plasma parity | Needs **Canvas (S5)** + structure + tokens + motion together |

## Revised Phase S emphasis

| Slice | Focus | Status |
|-------|--------|--------|
| **S3a** | Nav + placement + tone (chrome) | Done |
| **S3b** | Footer + Page chrome padding + Hero/Section spacing | Done |
| **S3** | Type/space/elevation tokens | Done |
| **S4** | Layout intents richer (align/gap/pad/split variants) | Done |
| **S4m** | Motion presets (`enter` / `press` / `reveal`) | Done |
| **S5** | Canvas / WebGL | Done |
| **S2** | Form controls | Done |
| **S6** | Image, Icon, Meta, drawer menu, RWD polish | Done |

## Consequences

- Roadmap treats **structure + chrome + presentation + motion** as one product arc — now delivered in `0.4.0`.
- Demo (`demo/app.py`) dogfoods the full stack (Nav + tokens + layout + motion + Canvas + Meta/Footer).
- Reject feature requests that only add unstyled tags without emit CSS + defaults.
