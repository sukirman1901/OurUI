# Spec Status

Status ladder:

| Status | Meaning |
|---|---|
| **Experimental** | May change freely; not relied upon |
| **Draft** | Intended direction; expect revisions |
| **Stable** | Safe to depend on within a major version |
| **Frozen** | Must not change until the next major version |

## Current status

Promoted **Phase M** (`spec-p0-stable`): P0 implemented surfaces are **Stable**. Production runtime hardening remains **Experimental**.

| Area | Status |
|---|---|
| Vision | Stable |
| Design Principles | Stable |
| Invariants + LOCKED + vocabulary | Stable |
| Compilation Architecture | Stable |
| RFC Process | Stable |
| Language Spec (P0 subset) | Stable |
| Semantic Graph (P0) | Stable (`ourui dump`) |
| DependencyGraph view (P0) | Stable (`ourui dump`) |
| IIR (P0) | Stable (`ourui dump`) |
| Node identity schema | Stable |
| `ourui dump` CLI | Stable |
| LTR | Stable (Layout Lowering in `ourui dump`) |
| RTR / HostNode | Stable (Render Lowering in `ourui dump`) |
| HTML emitter | Stable (`ourui emit`) |
| CSS emit | Stable (inlined + bundle) |
| JS emit / runtime shim | Stable (fetch RPC) |
| `@server` / `on_click` | Stable |
| `ourui serve` + RPC | Stable |
| `State` / binds | Stable |
| Components (expand) | Stable |
| HMR (`ourui serve`) | Stable |
| Routing (`route=` on `ui.Page`) | Stable |
| LSP | Stable (`ourui lsp` — completions + hover) |
| Runtime (production) | Experimental |

Update this table when phases land and when RFCs/ADRs promote artifacts to Stable/Frozen. Breaking changes to Stable artifacts in `0.x` require an ADR and a dump schema version bump when applicable — see [ADR-001](docs/decisions/ADR-001-p0-spec-stable.md).
