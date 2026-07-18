# ADR-004: OurUI-native design tokens

**Status:** Accepted  
**Date:** 2026-07-18  
**Tag:** `compiler-p0p`

## Context

VISION requires design tokens as first-class concepts. Emit used hard-coded hex. We want CSS variables without copying a third-party token sheet or mandating oklch.

## Decision

1. Ship a small OurUI token set (`bg`, `fg`, `primary`, `primary_fg`, `muted`, `border`, `card`, `accent`, `danger`, spacing, radius) with **hex/px** defaults.
2. Prefix all CSS vars with `--ourui-`; emit both `:root` and `.dark`.
3. Author via `ui.Theme(...)` overrides; Analyze stores `tokens.light` / `tokens.dark` on the Semantic Graph.
4. Bump dump schema to **version 9**.
5. Map `color=` / `variant=` / `bg=` role names to tone utility classes that consume the vars.

## Consequences

- Apps can theme without raw CSS while staying OurUI-native.
- Hosts may set `class="dark"` on `<html>` to switch maps; no toggle widget is shipped yet.
- Extending the key set should prefer ADR over silent dump changes.
