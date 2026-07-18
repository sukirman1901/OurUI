# ADR-013: Style Intent Catalog

- **Status:** Accepted (implementation through `ourui` **1.11.1**; catalog **1.11.0** — **L3 complete**, **0 C**)
- **Date:** 2026-07-18
- **Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-004](ADR-004-design-tokens.md), [ADR-012](ADR-012-motion-vocabulary.md), [ADR-014](ADR-014-language-primitives-vs-kit.md)

> **Product note:** This ADR is the package foundation. Example: `aspect="video"` → emit `.ourui-aspect-video` (`aspect-ratio: 16 / 9`). `ui.Theme` is a thin brand sheet — not this catalog. Coverage audit notes live in [`tailwind-gap.md`](../architecture/tailwind-gap.md) (evidence vs an external TOC — not the authoring API).

## Context

Dogfooding showed OurUI host craft lagging hand-authored CSS. Copying Tailwind’s **utility class API** (or `sv add tailwindcss` / `@tailwindcss/vite`) would resurrect class-string authoring in Python. Ignoring Tailwind’s **proven scales and CSS values** forces the project to invent mediocre tokens.

The Vite install doc only bootstraps Tailwind; the real surface is the utility TOC (Layout → Accessibility) — e.g. aspect-ratio.

## Decision

1. **Adopt Tailwind CSS values and scales** into `--ourui-*` ([`design/scales.py`](../../packages/ourui/ourui/design/scales.py)).
2. **Expose OurUI intent props** (`width=`, `pad_x=`, `grow=`, `aspect=`, `blur=`, …) — never `class="w-lg"` / `class="aspect-video"`.
3. **Emit finite `.ourui-*` utilities** generated from scales ([`design/style_intents.py`](../../packages/ourui/ourui/design/style_intents.py)).
4. **Coverage matrix** ([`design/style_catalog.py`](../../packages/ourui/ourui/design/style_catalog.py)): every TOC category is **A** (author), **B** (host), **C** (escape/subset), or combination — no silent gaps.
5. **Custom:** `ui.Theme` overrides + allowlisted CSS literals on props + `Theme(css=)` author sheet (app CSS without editing the package).

## Non-goals

- `@tailwindcss/vite` as OurUI runtime dependency
- Class detection / `@apply` / utility soup in Python
- Pixel-parity with every arbitrary Tailwind variant on day one for **C**-status rows (must still be listed)
- Shipping composed section patterns inside Stable `ui.*` (see ADR-014)

## Consequences

- Language surface grows; dump/schema may note `emit.style_intents`.
- Host CSS size grows (finite tables) — acceptable vs incomplete craft.
- Motion remains ADR-012 (`motion=`); transitions/animations map there first.
- Foundation work continues until the A/B matrix is honestly complete.
