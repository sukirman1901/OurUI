# ADR-012: Motion vocabulary (`family.pattern`)

**Status:** Accepted  
**Date:** 2026-07-18  
**Relates:** [ADR-005](ADR-005-intent-emit-escape.md), [ADR-007](ADR-007-site-structure-stack.md)

## Context

S4m shipped three coarse presets (`enter` / `reveal` / `press`). Product direction needs a **named motion vocabulary** authors can call (e.g. text word reveal) without prescribing layout (“header must animate like X”) and without installing a third-party motion package registry.

Smoothness matters more than dumping 100+ half-broken CSS rules.

## Decision

1. **Authoring:** `motion="family.pattern"` (e.g. `text.word-reveal`, `reveal.fade-up`).
2. **Registry:** `ourui.design.motion` holds the full catalog (≈12 families, 100+ patterns). Status per pattern: `stable` | `experimental`.
3. **Emit:** Only `stable` + `emit=True` patterns ship CSS/JS (phase **M1**). Experimental names are accepted in analysis (language surface) but have no host effect until later phases.
4. **M0 tokens:** Host CSS exposes `--ourui-motion-ease`, `--ourui-motion-duration-fast|…|slow` for consistent timing.
5. **Legacy aliases (Stable forever in 1.x):**
   - `enter` → `reveal.fade-up`
   - `reveal` → `reveal.mask-wipe`
   - `press` → `press.scale`
6. **A11y:** All emitted motion respects `prefers-reduced-motion: reduce`.
7. **Non-goals:** Raw keyframes / Framer API in author surface; “header must use pattern X”; registry-install DX.

## M1 Stable patterns (ship emit)

`reveal.fade-up`, `reveal.fade`, `reveal.mask-wipe`, `press.scale`, `hover.lift`, `hover.underline-slide`, `text.line-mask`, `text.fade-up`, `text.word-reveal`, `feedback.toast-slide`, `feedback.success-pulse`, `scroll.fade-in-view`.

## M2 Stable patterns (marketing emit)

`reveal.split`, `reveal.curtain`, `reveal.ink`, `reveal.stagger-children`, `reveal.blur-in`, `reveal.scale-fade`, `text.char-reveal`, `text.typewriter`, `text.marquee`, `text.underline-reveal`, `text.gradient-shift`, `flow.logo-marquee`, `hover.glow`, `hover.color-shift`, `spotlight.dim-siblings`, `micro.skeleton-shimmer`, `hero.stagger-copy`.

## M3 Stable (full catalog remainder)

All remaining registered patterns ship host CSS/JS approximations (catalog **1.2.0**). Complex morph/3D are simplified intentional presets — not full scene graphs.

Catalog version **1.2.0** — 146 Stable.

## Consequences

- Analysis stores **canonical** motion ids after alias resolve.
- Emit classes: `ourui-motion-{family}-{pattern}` (dots → dashes).
- Dump schema **30** (additive): `emit.motion`, attestation includes motion catalog version.
- Later **M2/M3+** promote Experimental → Stable with emit; no authoring API break.

## Alternatives rejected

| Option | Why not |
|--------|---------|
| Flat `motion="word-reveal"` only | Collides across families; weak LSP grouping |
| Package/block install for each pattern | Violates language-platform vision |
| Ship 100+ CSS on day one | Quality / bundle / a11y risk |
