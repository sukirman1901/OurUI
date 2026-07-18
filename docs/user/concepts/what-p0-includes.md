# What Stable includes

User docs under `docs/user/` document the **Stable** surface for `ourui` **1.6.0** (dump schema **28**) — P0 through Phase **S1–S6**, **T–W**, Enterprise **E1–E5**, and host security hardening.

## Included

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui check`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` + `ui.Link` |
| **Theme** | `ui.Theme` — color, type, space, elevation, density; `ui.ThemeToggle` |
| **Layout** | `ui.Shell` / `Section` — `layout=`, `gap=`, `pad=`, `align=`, `justify=` |
| **Chrome** | `ui.Nav` (placement/tone/drawer), `ui.Footer`, `ui.Meta` |
| **Forms** | `Input`, `Select`, `Toggle`, `Slider`, `Form` → `@server` payload |
| **Screens** | `Show` / `When`, Dialog, Toast, List/Table (static + dynamic) |
| **Motion** | `motion=enter\|press\|reveal` |
| **Escape** | `ui.Canvas` WebGL; `ui.Frame` (enterprise `SEC001` when using srcdoc) |
| **Polish** | `Image`, `Icon`, `Code`, `CopyButton`, `Menu`, control states |
| **Production serve** | `--prod`, `--workers N`, `--session-dir`; CSRF, rate limit, CSP nonce |
| **Trust** | Dump `attestation.sha256`, CSP baseline, enterprise check profile |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR (dev), LSP completions/hover |

See [Getting started](../getting-started.md) and the [Tutorial](../README.md#tutorial). API details: [Reference](../README.md#reference). Dogfood: `demo/app.py`. Gateway (auth outside `ui.*`): [examples/enterprise/gateway](../../../examples/enterprise/gateway/).

## Not in language scope (yet)

- **Redis / distributed sessions** — in-process or file-backed sessions
- **Auth / billing / data tables** — application concerns (see gateway + OIDC stub)
- **Client-only State** — browser-local without server round-trips
- **PDF / native hosts** — Host Contract is ready; emitters not shipped ([RFC-004](../../rfcs/RFC-004-second-host-pdf.md) Draft)
- **Published docs site** — this markdown tree *is* the Stable user guide

When a feature graduates to Stable, it appears in the tutorial, reference, [roadmap](../../roadmap.md), and [SPEC_STATUS.md](../../../SPEC_STATUS.md).
