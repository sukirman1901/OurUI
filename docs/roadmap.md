# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`. Capability generations (below) are the north-star framing; lettered phases A–S1 are historical P0 delivery.

## Capability generations

| Generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app (provisional host) | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done (`0.2.1`, dump schema 12) |
| **3 — Host** | Host consumes `RTR + Resolved Design` via a clean **Host Contract** | In progress — Spike B Done (`0.2.2`); `0.3.0` next |

```text
0.2.2 (emit reads RD)  →  finish contract-primary emit  →  0.3.0
```

**Not** on the critical path: Material packs, Plasma parity, `ui.Nav`, CSS AST-as-gate.

Bottleneck today:

```text
Resolved Design  →  Host Contract  →  HTML / CSS / JS
```

(Emit still provisional: `RTR + Theme + _BASE_CSS`.)

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
| **Host R&D (Gen 3)** | [RFC-003](rfcs/RFC-003-host-emit.md) Spike B (`0.2.2`) → contract-primary → `0.3.0` | In progress |

ADRs 005–007 record intent+emit+escape product notes. Sequencing of Presentation / Design System / Host is owned by the RFC ladder (001 → 002 → 003).
