# Spec Status

Status ladder:

| Status | Meaning |
|---|---|
| **Experimental** | May change freely; not relied upon |
| **Draft** | Intended direction; expect revisions |
| **Stable** | Safe to depend on within a major version |
| **Frozen** | Must not change until the next major version |

## Current status

| Area | Status |
|---|---|
| Vision | Stable |
| Design Principles | Stable |
| Invariants + LOCKED + vocabulary | Stable |
| Compilation Architecture | Stable |
| RFC Process | Stable |
| Language Spec (P0 subset) | Draft |
| Semantic Graph (P0) | Draft (implemented in `ourui dump`) |
| DependencyGraph view (P0) | Draft (implemented in `ourui dump`) |
| IIR (P0) | Draft (implemented in `ourui dump`) |
| Node identity schema | Draft |
| `ourui dump` CLI | Draft |
| LTR | Draft (Phase C — Layout Lowering in `ourui dump`) |
| RTR / HostNode | Draft (Phase D — Render Lowering in `ourui dump`) |
| HTML emitter | Draft (`ourui emit`) |
| CSS emit | Draft (inlined + bundle) |
| JS emit / runtime shim | Draft (Phase F/G — fetch RPC) |
| `@server` / `on_click` | Draft |
| `ourui serve` + RPC | Draft |
| `State` / binds | Draft (Phase H) |
| Components (expand) | Draft (Phase I) |
| HMR (`ourui serve`) | Draft (Phase J) |
| Runtime (production) | Experimental |
| LSP | Experimental |

Update this table when phases land and when RFCs promote artifacts to Stable/Frozen.
