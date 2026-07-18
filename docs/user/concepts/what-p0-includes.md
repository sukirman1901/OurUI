# What Stable includes

User docs under `docs/user/` document the **Stable** language surface for `ourui` **1.11.1** (dump schema **30**).

**Focus:** the package is an **intent → HTML/CSS/JS** compiler. Style-intent catalog **L3 complete**. See [VISION.md](../../../VISION.md).

## Included (Stable surface)

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui check`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` + `ui.Link` |
| **Style intents** | Utility props (`width=`, `aspect=`, `pad_x=`, `grow=`, …) — ADR-013 |
| **`ui.Theme`** | Thin brand roles — color, type, space, elevation, density, `page=`, `css=` |
| **Layout** | `ui.Shell` / `Section` — `layout=`, `gap=`, `pad=`, `align=`, `justify=` + style intents |
| **Chrome (thin)** | `ui.Nav`, `ui.Footer`, `ui.Meta`; full-bleed via `Theme(page=…)` |
| **Forms** | `Input`, `Select`, `Toggle`, `Slider`, `Form` → `@server` payload |
| **Screens** | `Show` / `When`, Dialog, Toast, List/Table (static + dynamic) |
| **Motion** | `motion=family.pattern` (146 Stable patterns, catalog 1.2.0) |
| **Escape** | `ui.Canvas` WebGL; `ui.Frame` (`SEC001` under `--profile a11y`); `Theme(css=)` |
| **Polish** | `Image`, `Icon`, `Code`, `CopyButton`, `Menu`, control states |
| **Production serve** | `--prod`, `--workers N`, `--session-dir`; CSRF, rate limit, CSP nonce |
| **Trust** | Dump `attestation.sha256`, CSP baseline, `ourui check --profile a11y` |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR (dev), LSP completions/hover (incl. style intent values) |

Samples: `examples/tutorial/`, `examples/landing/` (dogfood). Auth outside language: [examples/gateway](../../../examples/gateway/).

## Honest limits

- Host chrome defaults are opinionated emit CSS, not “tokens alone solve craft”
- Arbitrary beyond allowlists → `Theme(css=)` / `Canvas` / `Image`

## Out of language scope

- Redis / distributed sessions
- Auth / billing / data tables — application concerns ([gateway](../../../examples/gateway/))
- Composed section patterns inside Stable `ui.*` ([ADR-014](../../decisions/ADR-014-language-primitives-vs-kit.md))
- Class-string CSS authoring as the Stable API
