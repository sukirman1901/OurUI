# ADR-002: Single-process prod serve with session State

**Status:** Accepted  
**Date:** 2026-07-18  
**Tag:** `compiler-p0n`

## Context

`ourui serve` was a dev server: HMR always on, module-global `State` shared by all clients, and 500 responses leaked Python tracebacks. SPEC_STATUS listed Runtime (production) as Experimental.

## Decision

1. Add `ourui serve --prod` for **single-process** production:
   - no HMR / file watcher
   - session-scoped State via HttpOnly cookie `ourui_sid` + in-memory `SessionStore`
   - no `traceback` in client JSON errors (stderr only)
   - `GET /__ourui/health`
2. Keep default `ourui serve` as **dev** (process-global State + HMR) for compatibility.
3. Serialize session hydrate → handler → persist under a process lock so concurrent requests are safe.
4. **Defer** multi-worker and shared stores (Redis, etc.) — remain Experimental.

## Consequences

- Multi-user demos on one process no longer clobber each other’s State.
- Horizontal scale still requires a future shared-session design (ADR/RFC).
- Runtime (single-process prod) is Stable; Runtime (multi-worker) stays Experimental.
