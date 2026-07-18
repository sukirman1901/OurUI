# ADR-004: OurUI-native theme roles (design tokens)

**Status:** Accepted — **narrowed by [ADR-013](ADR-013-style-intent-catalog.md)**  
**Date:** 2026-07-18  
**Tag:** `compiler-p0p`

> **Scope note:** This ADR covers the thin `--ourui-*` **theme role** sheet via `ui.Theme` (color, density, page measure, legacy space/type keys). **Craft depth** is the utility catalog (ADR-013) — e.g. aspect-ratio → `aspect=`. See [VISION.md](../../VISION.md).

## Context

VISION originally required design tokens as first-class concepts. Emit used hard-coded hex. We want CSS variables without copying a third-party token sheet or mandating oklch.

## Decision

1. Ship a small OurUI token set (`bg`, `fg`, `primary`, `primary_fg`, `muted`, `border`, `card`, `accent`, `danger`, spacing, radius) with **hex/px** defaults.
2. Prefix all CSS vars with `--ourui-`; emit both `:root` and `.dark`.
3. Author via `ui.Theme(...)` overrides; Analyze stores `tokens.light` / `tokens.dark` on the Semantic Graph.
4. Bump dump schema to **version 9**.
5. Map `color=` / `variant=` / `bg=` role names to tone utility classes that consume the vars.

## Consequences

- Apps can theme brand roles without raw CSS while staying OurUI-native.
- Hosts may set `class="dark"` on `<html>` to switch maps; `ui.ThemeToggle` is the client control.
- Extending the key set should prefer ADR over silent dump changes.
- Do not treat this sheet as a substitute for Tailwind-depth utilities (ADR-013).
