# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`. Capability generations (below) are the north-star framing; lettered phases A–S1 are historical P0 delivery.

## Capability generations

| Generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app (provisional host) | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done (`0.2.1`, dump schema 12) |
| **3 — Host** | Host consumes `RTR + Resolved Design` via **Host Contract** | **Done (`0.3.0`)** |

```text
Gen 1–3 complete. S1–S2 + S3a Nav shipped. Next optional: S3 tokens / S5 Canvas / S6 polish.
```

## Historical phases (P0)

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
| **Presentation R&D** | [RFC-001](rfcs/RFC-001-presentation-system.md); Graph in dump (schema 11, `0.2.0`) | Done |
| **Design System R&D** | [RFC-002](rfcs/RFC-002-design-system.md); `resolved_design` (schema 12, `0.2.1`) | Done |
| **Host R&D (Gen 3)** | [RFC-003](rfcs/RFC-003-host-emit.md) contract-primary emit | **Done (`0.3.0`)** |
| **S2** | Form controls: `Input` / `Select` / `Toggle` / `Slider` → `@server` (schema 14, `0.3.2`) | Done |
| **S3a** | `ui.Nav` + `placement=` + `tone=` (schema 15, `0.3.3`) | Done |

ADRs 005–007 record intent+emit+escape product notes. Next optional: S3 tokens, S5 Canvas, or S6 polish.
