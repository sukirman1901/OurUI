# ADR-010: Show / When + dynamic List/Table (Enterprise E1)

- **Status:** Accepted
- **Date:** 2026-07-18
- **Package:** `ourui` 1.1.0 · dump schema **26** (additive)

## Context

Enterprise screens need conditional UI and lists driven by `State`, without adopting a client VDOM (Reflex/React model). Dialog already proves the pattern: boolean State → bind → host attribute → CSS.

## Decision

1. **`ui.Show(show=State|bool, *children)`** — emit a wrapper; toggle `data-show`; children always in DOM (Dialog twin).
2. **`ui.When(show=, then=, else_=)`** — emit both branches; host shows `then` or `else` from the same bind.
3. **`ui.List(items=State)` / `ui.Table(columns=static, rows=State)`** — initial SSR from State snapshot; `applyState` rebuilds `<li>` / `<tr>` from JSON arrays (strings or plain dicts). No nested `ui.*` item templates in E1.
4. Host remains a thin RPC + DOM patch shim — not a component framework.

## Consequences

- Dump schema bumps to **26** with `emit.show` / `emit.when` / `emit.dynamic_list`.
- Additive for 1.x consumers; unknown kinds ignored by older tools.
- Nested component-per-row deferred; file upload deferred to later E1+/E2.

## Alternatives rejected

- Drop inactive branches from RTR (breaks SSR seed + applyState).
- Client-side `foreach` with React-like reconciliation.
