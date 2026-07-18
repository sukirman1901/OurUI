# What Stable includes

User docs under `docs/user/` document the **Stable** surface for `ourui` **1.9.1** (dump schema **30**) — P0 through Phase **S1–S6**, **T–W**, Enterprise **E1–E5**, host security, motion (ADR-012), and the Style Intent Catalog (ADR-013).

## Included

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui check`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` + `ui.Link` |
| **Theme** | `ui.Theme` — color, type, space, elevation, density, scale overrides (`space=` / `sizes=` / `type=`); `ui.ThemeToggle` |
| **Layout** | `ui.Shell` / `Section` — `layout=`, `gap=`, `pad=`, `align=`, `justify=` plus style intents (`width=`, `grow=`, `grid_cols=`, …) |
| **Chrome** | `ui.Nav` (placement/tone/drawer), `ui.Footer`, `ui.Meta`; recipe `marketing` for full-bleed |
| **Forms** | `Input`, `Select`, `Toggle`, `Slider`, `Form` → `@server` payload |
| **Screens** | `Show` / `When`, Dialog, Toast, List/Table (static + dynamic) |
| **Motion** | `motion=family.pattern` (146 Stable patterns, catalog 1.2.0) |
| **Escape** | `ui.Canvas` WebGL; `ui.Frame` (enterprise `SEC001` when using srcdoc) |
| **Polish** | `Image`, `Icon`, `Code`, `CopyButton`, `Menu`, control states |
| **Production serve** | `--prod`, `--workers N`, `--session-dir`; CSRF, rate limit, CSP nonce |
| **Trust** | Dump `attestation.sha256`, CSP baseline, enterprise check profile |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR (dev), LSP completions/hover (incl. style intent values) |

See [Getting started](../getting-started.md) and the [Tutorial](../README.md#tutorial). API details: [Reference](../README.md#reference). Samples: `examples/tutorial/`, `examples/enterprise/`, `examples/landing/`. Gateway (auth outside `ui.*`): [examples/enterprise/gateway](../../../examples/enterprise/gateway/).

## Not in language scope

- **OurUI Kit / block registry** — out of language ([ADR-014](../../decisions/ADR-014-language-primitives-vs-kit.md)); compose primitives in app code
- **Redis / distributed sessions** — in-process or file-backed sessions
- **Auth / billing / data tables** — application concerns (see gateway + OIDC stub)
- **Client-only State** — browser-local without server round-trips
- **PDF / native hosts** — Host Contract is ready; emitters not shipped ([RFC-004](../../rfcs/RFC-004-second-host-pdf.md) Draft)
- **Published docs site** — this markdown tree *is* the Stable user guide
- **True escape craft** — mix-blend, mask, arbitrary background-image (catalog **C**)

When a feature graduates to Stable, it appears in the tutorial, reference, [roadmap](../../roadmap.md), and [SPEC_STATUS.md](../../../SPEC_STATUS.md).
