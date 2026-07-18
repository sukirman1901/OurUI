# What Stable includes

User docs under `docs/user/` document the **Stable** language surface for `ourui` **1.11.0** (dump schema **30**).

**Focus now:** the package is a **utility → HTML/CSS/JS** compiler. The style-intent catalog is **still incomplete** — that is the foundation work. See [VISION.md](../../../VISION.md).

## Included (Stable surface)

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui check`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` + `ui.Link` |
| **Style intents** | Utility props (`width=`, `aspect=`, `pad_x=`, `grow=`, …) — catalog filling (ADR-013) |
| **`ui.Theme`** | Thin brand roles — color, type, space, elevation, density, `page=` |
| **Layout** | `ui.Shell` / `Section` — `layout=`, `gap=`, `pad=`, `align=`, `justify=` + style intents |
| **Chrome (thin)** | `ui.Nav`, `ui.Footer`, `ui.Meta`; full-bleed via `Theme(page=…)` |
| **Forms** | `Input`, `Select`, `Toggle`, `Slider`, `Form` → `@server` payload |
| **Screens** | `Show` / `When`, Dialog, Toast, List/Table (static + dynamic) |
| **Motion** | `motion=family.pattern` (146 Stable patterns, catalog 1.2.0) |
| **Escape** | `ui.Canvas` WebGL; `ui.Frame` (`SEC001` under `--profile a11y`) |
| **Polish** | `Image`, `Icon`, `Code`, `CopyButton`, `Menu`, control states |
| **Production serve** | `--prod`, `--workers N`, `--session-dir`; CSRF, rate limit, CSP nonce |
| **Trust** | Dump `attestation.sha256`, CSP baseline, `ourui check --profile a11y` |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR (dev), LSP completions/hover (incl. style intent values) |

Samples: `examples/tutorial/`, `examples/landing/` (dogfood). Auth outside language: [examples/gateway](../../../examples/gateway/).

## Foundation gaps (honest)

- Style Intent Catalog **L3 shipped** — niche **C** remain ([style intents](../reference/style-intents.md))
- Host chrome defaults are opinionated emit CSS, not “tokens solved craft”

## Out of language scope

- Redis / distributed sessions
- Auth / billing / data tables — application concerns ([gateway](../../../examples/gateway/))
- Composed section patterns inside Stable `ui.*` while foundation is incomplete ([ADR-014](../../decisions/ADR-014-language-primitives-vs-kit.md))
- Client-only State — browser-local without server round-trips
- PDF / native hosts — Host Contract ready; emitters not shipped ([RFC-004](../../rfcs/RFC-004-second-host-pdf.md) Draft)
- Published docs site — this markdown tree *is* the Stable user guide
- True escape craft — mix-blend, mask, arbitrary background-image (catalog **C**)

When a feature graduates to Stable, it appears in the tutorial, reference, [roadmap](../../roadmap.md), and [SPEC_STATUS.md](../../../SPEC_STATUS.md).
