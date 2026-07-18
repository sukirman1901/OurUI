# ADR-005: Presentation strategy — intent + emit + escape

**Status:** Accepted  
**Date:** 2026-07-18  
**Tag:** `compiler-p0s1` (S1 shipped; further S slices TBD)

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

| Slice | Deliverable |
|-------|-------------|
| **S1** | `ui.Link` + shell/layout intent (nav between routes; Studio-like regions) |
| **S2** | Controls: Input, Slider, Select, Toggle (+ form → `@server`) |
| **S3** | Deeper presentation tokens (type/space/elevation; theme toggle surface) |
| **S4** | Richer layout intents (`stack` / `row` / `grid` / `split-*`, gap/pad/align) |
| **S5** | Host escape: Canvas / WebGL (and optional scoped slot) |
| **S6** | Host polish: control states, responsive emit rules, Image/Icon/Meta |

Evidence for prioritization: `demo/GAPS.md` (Plasma-shaped dogfood).

## Consequences

- Visual quality rises **incrementally** with each slice; Plasma-class fidelity requires **S5**, not CSS utilities alone.
- Language Spec / emitters grow via RFC or ADR when HostNode attributes or dump schema change.
- usePyX remains a historical reference for what **not** to resurrect wholesale; useful ideas (`@var`/derived, forms) may return only as intent APIs under this ADR.
