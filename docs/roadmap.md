# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/` and have their own Draft → Accepted → Implemented lifecycle.

| Phase | Deliverable | Status |
|---|---|---|
| **A** | Documentation freeze → tag `docs-v1` | Done |
| **B–E** | Dump → IIR → LTR → RTR → HTML | Done |
| **F** | JS shim + `on_click` / `@server` | Done |
| **G** | `ourui serve` + HTTP RPC | Done |
| **H** | `State` bind + live updates | Done |
| **I** | Components expand | Done |
| **J** | HMR (SSE reload on file change) | Done |
| **K** | Multi-page routing (`route=` on `ui.Page`) | Done |
| **L** | Lightweight LSP (`ourui lsp`) | Done |
| **M** | Spec Stability Pass (P0 → Stable, tag `spec-p0-stable`) | Done |
| **N** | Production runtime (`serve --prod`, session State) | Done |
| **O** | Multi-worker + file session store (`--workers`, `--session-dir`) | Done |
| **P** | Design tokens (`ui.Theme`, `--ourui-*` CSS vars) — provisional | Done |
| **Q** | User documentation (`docs/user/`) | Done |
| **R** | Package release `0.1.0` / `0.1.1` | Done |
| **S1** | `ui.Link` + `ui.Shell` / `layout=` (dump schema 10, `0.1.2`) | Done |
| **Presentation R&D** | [RFC-001](rfcs/RFC-001-presentation-system.md) Accepted; Graph in dump (schema 11, `0.2.0`) | Done |
| **Design System R&D** | [RFC-002](rfcs/RFC-002-design-system.md) Accepted; `resolved_design` in dump (schema 12, `0.2.1`) | Done |
| **Host Emit R&D** | [RFC-003](rfcs/RFC-003-host-emit.md) Stub → Draft | Next |

ADRs 005–007 record intent+emit+escape product notes; sequencing of Presentation / Design System / Host is owned by the RFC ladder (001 → 002 → 003), not by further S3a–S6 chrome slices.
