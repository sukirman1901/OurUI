# What Stable includes

User docs under `docs/user/` document the **Stable** surface for `ourui` **0.4.0** (dump schema **21**) — historically called “P0” plus Phase **S1–S6**.

## Included

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` + `ui.Link` |
| **Theme** | `ui.Theme` — color, type, space, elevation tokens; `ui.ThemeToggle` |
| **Layout** | `ui.Shell` / `Section` — `layout=`, `gap=`, `pad=`, `align=`, `justify=` |
| **Chrome** | `ui.Nav` (placement/tone/drawer), `ui.Footer`, `ui.Meta` |
| **Forms** | `Input`, `Select`, `Toggle`, `Slider` → `@server` payload |
| **Motion** | `motion=enter\|press\|reveal` |
| **Escape** | `ui.Canvas` WebGL (gradient / dither / raymarch) |
| **Polish** | `Image`, `Icon`, `Code`, `CopyButton`, `Menu`, control states |
| **Production serve** | `--prod`, `--workers N`, `--session-dir` |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR, LSP completions/hover |

See [Getting started](../getting-started.md) and the [Tutorial](../README.md#tutorial). API details: [Reference](../README.md#reference). Dogfood: `demo/app.py`.

## Not in language scope (yet)

- **Redis / distributed sessions** — P0 uses in-process or file-backed sessions
- **Auth / billing / data tables** — application concerns
- **Client-only State** — browser-local without server round-trips
- **PDF / native hosts** — Host Contract is ready; emitters not shipped
- **Published docs site** — this markdown tree *is* the Stable user guide

When a feature graduates to Stable, it appears in the tutorial, reference, [roadmap](../../roadmap.md), and [SPEC_STATUS.md](../../../SPEC_STATUS.md).
