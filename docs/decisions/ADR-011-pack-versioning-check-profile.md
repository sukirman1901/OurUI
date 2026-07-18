# ADR-011: Pack versioning + `ourui check` profiles (Enterprise E2)

- **Status:** Accepted
- **Date:** 2026-07-18
- **Package:** `ourui` 1.5.0 · dump schema **27** (additive)

## Context

Org-scale products need a stable default pack identity (`ourui-default` + version) and density recipes, plus a lint profile that catches a11y gaps without failing every compile by default.

## Decision

1. **Pack version** — `default_pack()` includes `"version": "1.0.0"`; Resolved Design dumps `pack_version`.
2. **Density** — `ui.Theme(density="compact"|"comfortable")` is an analysis override; Resolved Design carries `density`; emit adds `ourui-density-compact` on `<html>` / `.ourui-root` and tightens space tokens via CSS.
3. **Check profiles** — `ourui check --profile default|enterprise`. Enterprise runs normal diagnostics plus `collect_enterprise_diagnostics` (label/alt/button text/escape budget). Warnings print with exit **0**; `--strict` promotes enterprise warnings to errors (exit 1).

## Consequences

- Dump schema **27** adds `emit.density` / `csp` / `attestation` and Resolved Design `pack_version` (+ optional `density`).
- Auth/SSO remain outside `ui.*` (see Enterprise Kit templates).

## Alternatives rejected

- Failing `ourui check` on all a11y warnings by default (too noisy for tutorials).
- Embedding pack lockfiles in the language (app-layer / CI concern).
