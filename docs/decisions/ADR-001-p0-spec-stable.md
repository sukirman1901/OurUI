# ADR-001: Promote P0 specs to Stable

**Status:** Accepted  
**Date:** 2026-07-18  
**Tag:** `spec-p0-stable`

## Context

Phases A–L shipped a working P0 compiler (`ourui dump` / `emit` / `serve` / `lsp`) with tests. Core documents were already Stable; language, IR, emitter, and runtime-dev surfaces remained Draft even though they were implemented. Leaving them Draft forever made “Done” feel incomplete and gave no compatibility signal.

## Decision

1. Promote all P0 implemented artifacts listed in [SPEC_STATUS.md](../../SPEC_STATUS.md) to **Stable**.
2. Keep **Runtime (production)** (multi-worker / production hardening) as **Experimental**.
3. Do **not** mark P0 surfaces **Frozen** — `0.x` may still refine them with process.
4. Breaking changes to Stable artifacts in `0.x` require:
   - a short ADR (or RFC if LOCKED vocabulary / Compilation Flow is touched), and
   - a dump schema version bump when serialized artifacts change.

## Consequences

- Downstream tools and docs may treat P0 Language Spec, OurIR stages, HTML emit, serve/RPC/HMR/routing, and lightweight LSP as dependable within major `0.x`.
- Production deployment story remains explicitly Experimental until a later phase.
- Feature work (Rust port, native/PDF emitters, full LSP diagnostics) stays out of this decision.
