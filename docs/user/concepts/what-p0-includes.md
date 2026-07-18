# What P0 includes

**Stable P0** is the supported surface for building real apps today. User docs under `docs/user/` document only this scope — not draft RFCs or future phases.

## Included in P0

| Area | What you can do |
|------|-----------------|
| **CLI** | `ourui dump`, `ourui emit`, `ourui serve`, `ourui lsp` |
| **State** | Server-backed `State` with bind paths and live updates over `serve` |
| **Server handlers** | `@server` functions invoked from the browser via HTTP RPC |
| **Routing** | Multiple pages with `ui.Page(..., route=...)` |
| **Theme** | `ui.Theme` and `color=` tokens emitted as `--ourui-*` CSS variables |
| **Production serve** | `--prod` for sessions and safe errors |
| **Multi-worker** | `--workers N` with file-backed sessions (`--session-dir`) |
| **Components** | Function components and `Component` classes |
| **Developer UX** | HMR on file change, LSP completions/hover for `ui.*`, `State`, `@server` |

See [Getting started](../getting-started.md) and the [Tutorial](../README.md#tutorial) for hands-on coverage. API details live in [Reference](../README.md#reference).

## Not yet in P0

These are planned or out of scope for the current stable release. Do not expect them to work without checking the roadmap or specs:

- **Forms** — structured form components and validation helpers
- **Redis session store** — distributed session backend (P0 uses in-process or file-backed sessions)
- **Client-only State** — state that lives entirely in the browser without server round-trips
- **PDF export** — server or client PDF generation from pages
- **Rust runtime** — alternate host implementation
- **Published docs site** — browsable site separate from in-repo markdown (this tree *is* the P0 user docs)

When a feature graduates to Stable P0, it will appear in the tutorial, reference, and [roadmap](../../roadmap.md).
