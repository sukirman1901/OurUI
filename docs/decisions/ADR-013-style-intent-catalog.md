# ADR-013: Style Intent Catalog — Tailwind TOC → OurUI intents

- **Status:** Accepted (implementation in `ourui` 1.9.x)
- **Date:** 2026-07-18
- **Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-004](ADR-004-design-tokens.md), [ADR-012](ADR-012-motion-vocabulary.md)

## Context

Dogfooding showed OurUI host craft lagging hand-authored CSS. Copying Tailwind’s **utility class API** (or `sv add tailwindcss` / `@tailwindcss/vite`) would resurrect “Tailwind in Python”. Ignoring Tailwind’s **proven scales and CSS values** forces the project to invent mediocre tokens.

The Vite install doc only bootstraps Tailwind; the real surface is the utility TOC (Layout → Accessibility).

## Decision

1. **Adopt Tailwind CSS values and scales** into `--ourui-*` ([`design/scales.py`](../../packages/ourui/ourui/design/scales.py)).
2. **Expose OurUI intent props** (`width=`, `pad_x=`, `grow=`, `blur=`, …) — never `class="w-lg"`.
3. **Emit finite `.ourui-*` utilities** generated from scales ([`design/style_intents.py`](../../packages/ourui/ourui/design/style_intents.py)).
4. **Coverage matrix** ([`design/style_catalog.py`](../../packages/ourui/ourui/design/style_catalog.py)): every TOC category is **A** (author), **B** (host), **C** (escape/subset), or combination — no silent gaps.
5. **Custom:** `ui.Theme` overrides + allowlisted CSS literals on props.

## Non-goals

- `@tailwindcss/vite` as OurUI runtime dependency
- Class detection / `@apply` / utility soup in Python
- Pixel-parity with every arbitrary Tailwind variant on day one for **C**-status rows (must still be listed)

## Consequences

- Language surface grows; dump/schema may note `emit.style_intents`.
- Host CSS size grows (finite tables) — acceptable vs incomplete craft.
- Motion remains ADR-012 (`motion=`); transitions/animations map there first.
