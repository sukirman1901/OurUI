# ADR-014: Language primitives first — foundation before composed patterns

- **Status:** Accepted
- **Date:** 2026-07-18
- **Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-013](ADR-013-style-intent-catalog.md)

## Context

Three layers get collapsed too easily:

1. **Language** — intent props, analysis, IR, emit, host contract  
2. **Utilities / host craft** — scales, style intents, thin chrome defaults (**foundation**)  
3. **Composed patterns** — full nav+menu sections, marketing stacks, marketplace components  

Shipping (3) into Stable `ui.*` freezes product UI into the grammar. Delaying (2) for (3) leaves craft half-done.

## Decision

1. **OurUI is intent primitives + host** — author `width=`, `aspect=`, `gap=`, `color=`, `layout=`, `motion=` — not Tailwind class strings, not a component marketplace.
2. **Craft depth = utility catalog** (ADR-013). `ui.Theme` is only a thin brand sheet.
3. **Composed patterns stay out of Stable `ui.*` for now.** Compose in app code (or a future out-of-tree package) from primitives + utilities.
4. **Near-term focus:** fill utility catalog, host defaults, prop docs/LSP; promote high-use **C → A**; keep true escapes as **C**.

## Non-goals (now)

- Component registry / copy-paste CLI inside `ourui`
- Growing Stable `ui.*` with section patterns
- Replacing intent props with `class=` authoring

## Consequences

- Docs say “utilities first”; reject “add this as ui.X” when X is a composed pattern.
- Escape (`Canvas`, `Frame`, catalog C) remains the valve for one-off craft.
- `examples/landing` is dogfood composition, not a shipped product surface.
