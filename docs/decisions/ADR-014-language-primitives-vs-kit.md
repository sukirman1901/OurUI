# ADR-014: Language primitives first — Kit stays out of language

- **Status:** Accepted
- **Date:** 2026-07-18
- **Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-013](ADR-013-style-intent-catalog.md)

## Context

OurUI needs a clear product boundary. Teams often collapse three layers into one:

1. **Language** — intent props, analysis, IR, emit, host contract  
2. **Design scales / host craft** — tokens, utilities, chrome defaults  
3. **Component kit** — Card patterns, landing blocks, “shadcn-like” recipes  

Shipping (3) inside `ui.*` Stable would freeze opinionated product UI into the grammar, swell the surface, and make 1.x versioning painful. Delaying (1)–(2) for a kit would leave the language half-done.

## Decision

1. **OurUI is a language of intent primitives** (plus host that realizes them). Author writes `width=`, `gap=`, `color=`, `layout=`, `motion=` — not Tailwind class strings, not a component marketplace.
2. **Scales and coverage stay Tailwind-class in depth** (ADR-013): complete A/B/C matrix, finite `.ourui-*` emit, `ui.Theme` overrides. This is what makes the language scalable *without* a kit.
3. **OurUI Kit (shadcn / Svelte-UI analogue) is explicitly out of scope for the language package.** When it exists, it lives **outside** the Stable grammar — examples, a separate package, or app-level components that *call* OurUI primitives. Kit must not become new `ui.Foo` kinds by default.
4. **Near-term focus (no kit):** host defaults, prop docs/LSP, promote high-use catalog **C → A** where intent props are the right fix; keep true escape rows as **C** (blend, mask, arbitrary bg-image).

## Non-goals (now)

- Block registry / copy-paste component CLI inside `ourui`
- Growing Stable `ui.*` with marketing section kits
- Replacing intent props with `class=` authoring

## Consequences

- Docs and ADRs say “primitives first”; contributors reject “add this as ui.X” when X is a kit pattern.
- Kit work starts only after language+host feels proper for composition.
- Escape (`Canvas`, `Frame`, catalog C) remains the valve for one-off craft.
