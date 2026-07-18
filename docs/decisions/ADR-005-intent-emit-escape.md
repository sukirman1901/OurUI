# ADR-005: Presentation strategy — intent + emit + escape

**Status:** Accepted + **Implemented (S1–S6 complete, `0.4.0`)**  
**Date:** 2026-07-18  
**Tag:** `compiler-p0s1` → Phase S closed at package `0.4.0` / dump schema **21**

## Context

Dogfooding a Plasma-shaped SaaS demo (`demo/`) showed a large visual/UX gap versus hand-authored HTML/CSS/JS (and versus prior experiment [usePyX](https://github.com/sukirman1901/usePyX)).

Three options were considered:

| Option | Idea | Rejected because |
|--------|------|------------------|
| **A** | Expose full CSS/Tailwind utility surface in Python | Recreates usePyX “HTML/Tailwind berkedok Python”; breaks intent-over-markup |
| **B** | Richer **intent** → richer **emit** + limited **escape** | — chosen |
| **C** | OurUI for logic only; keep Plasma as separate HTML stack | Permanently splits the product vision |

## Decision

Adopt **B** for all post-P0 presentation work:

1. **Intent** — authors express layout, chrome, controls, and theme in Python (`ui.*` / props), not DOM tags or utility class strings.
2. **Emit** — the compiler owns Flex/Grid/spacing/type/hover/responsive CSS derived from those intents and from `--ourui-*` tokens (extend tables; do not dump the Tailwind catalog into the language).
3. **Escape** — first-class host escapes only where intent cannot honestly cover the host (e.g. `ui.Canvas` / WebGL for Plasma-class tools). Escapes are explicit, documented, and do not become the default styling path.

Explicit non-goals:

- `ui.div` / `ui.span` as the primary authoring model (usePyX path)
- `.style(bg="blue-500", p=4)` / className utility soup as Stable API
- Parity with the full CSS property/utility encyclopedia before shipping smaller intent slices

## Phase S slices (implementation order)

| Slice | Deliverable | Status |
|-------|-------------|--------|
| **S1** | `ui.Link` + shell/layout intent | Done |
| **S2** | Controls: Input, Slider, Select, Toggle | Done |
| **S3a** | `ui.Nav` + placement + tone | Done |
| **S3** | Type/space/elevation tokens; ThemeToggle | Done |
| **S3b** | Footer + Hero/Section pad rhythm | Done |
| **S4** | Richer layout (`gap`/`pad`/`align`/`split-*`) | Done |
| **S4m** | Motion presets | Done |
| **S5** | Host escape: Canvas / WebGL | Done |
| **S6** | Host polish: states, Image/Icon/Meta, drawer | Done |

Evidence: early Plasma-shaped dogfood gaps (language gaps closed; Redis/auth remain app-scope).

## Consequences

- Visual quality rose incrementally with each slice; Plasma-class living backgrounds use **S5 Canvas**, not CSS utilities alone.
- Language Spec / emitters grow via RFC or ADR when HostNode attributes or dump schema change.
- usePyX remains a historical reference for what **not** to resurrect wholesale; useful ideas (`@var`/derived, forms) may return only as intent APIs under this ADR.
