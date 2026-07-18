# ADR-011: Density + `ourui check` profiles

- **Status:** Accepted (pack API superseded)
- **Date:** 2026-07-18
- **Package:** `ourui` 1.5.0 · dump schema **27** (later **28** adds security / `attestation.sha256`)
- **Note (`1.10.0`):** Theme seed is `ourui.theme` only. Density + `Theme(page=)` + check profiles remain. Profile name: **`a11y`**. See [CHANGELOG](../../CHANGELOG.md) `1.10.0`.

## Context

Products need density control and a lint profile for a11y gaps without failing every compile by default.

## Decision (current)

1. **Density** — `ui.Theme(density="compact"|"comfortable")`; Resolved Design carries `density`; emit adds `ourui-density-compact` and tightens space tokens.
2. **Page measure** — `ui.Theme(page={...})`; `max_width: none` → full-bleed.
3. **Check profiles** — `ourui check --profile default|a11y`. Profile `a11y` adds label/alt/button/escape diagnostics. Warnings exit **0**; `--strict` → errors (exit 1).

## Historical (removed)

At 1.5–1.7 the language briefly exposed named theme packs / recipes and `pack_version` on Resolved Design. That API was removed in **1.10.0** — craft depth is style intents, not pack catalogs.

## Consequences

- Dump may carry `density` / `page` on Resolved Design; attestation has schema / motion_catalog / `sha256` (no pack fields).
- Auth/SSO remain outside `ui.*` ([`examples/gateway/`](../../examples/gateway/)).

## Alternatives rejected

- Failing `ourui check` on all a11y warnings by default (too noisy for tutorials).
