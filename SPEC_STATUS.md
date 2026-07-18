# Spec Status

Status ladder:

| Status | Meaning |
|---|---|
| **Experimental** | May change freely; not relied upon |
| **Draft** | Intended direction; expect revisions |
| **Stable** | Safe to depend on within a major version |
| **Frozen** | Must not change until the next major version |

## Current status

Promoted **Phase M** (`spec-p0-stable`): P0 implemented surfaces are **Stable**.  
**Phase N** (`compiler-p0n`): single-process production serve is **Stable**.  
**Phase O** (`compiler-p0o`): file-backed multi-worker serve is **Stable** (Unix `fcntl`).  
**Phase P** (`compiler-p0p`): OurUI design tokens (`--ourui-*`) are **Stable**.  
**Phase R** (`v0.1.0` / `compiler-p0r`): first package release of the `ourui` compiler/runtime on PyPI-ready packaging (local install / wheel build; not necessarily published).  
**Phase S1** (`compiler-p0s1` / `v0.1.2`): `ui.Link` + `ui.Shell` / `layout=` — Stable (dump schema **10**).  
**RFC-001** (`v0.2.0`): Presentation Graph in dump (schema **11**, Option A).  
**RFC-002** (`v0.2.1`): Resolved Design in dump (schema **12**).  
**RFC-003** (`v0.3.0`): Host Contract Implemented — emit **requires** `RTR + Resolved Design`.  
**Phase S2** (`v0.3.1`): `ui.Input` + form → `@server` (dump schema **13**).

### Capability generations

| Generation | Status |
|---|---|
| 1 — Language infrastructure | Done |
| 2 — Semantic presentation (PG + DS → Resolved Design) | Done (`0.2.1`) |
| 3 — Host (`RTR + Resolved Design` via Host Contract) | **Done (`0.3.0`)** |

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
| HTML emitter | Stable — Host Contract primary (`RTR + Resolved Design` required) |
| CSS emit | Stable — from Resolved Design; `_BASE_CSS` = host-private chrome only |
| Design tokens (`ui.Theme`) | Stable (Phase P) — overrides flow into Design System resolve |
| JS emit / runtime shim | Stable (fetch RPC) |
| `@server` / `on_click` | Stable |
| `ourui serve` + RPC | Stable |
| `State` / binds | Stable |
| Components (expand) | Stable |
| HMR (`ourui serve`) | Stable |
| Routing (`route=` on `ui.Page`) | Stable |
| LSP | Stable (`ourui lsp` — completions + hover + tokens) |
| Runtime (single-process prod) | Stable (`ourui serve --prod`) |
| Runtime (multi-worker, file store) | Stable (`--prod --workers N`, `--session-dir`) |
| Package (`ourui` 0.3.1) | Stable ([PyPI](https://pypi.org/project/ourui/); Host Contract + `ui.Input`) |
| Presentation Graph | Stable (RFC-001 Option A — lowering) |
| Resolved Design | Stable (RFC-002 — dump + required emit input) |
| Design System pack (`ourui-default`) | Draft (seeded from `theme.py`; packs API may grow) |
| Host Contract | Stable (RFC-003 Implemented) |
| `ui.Link` / `ui.Shell` / `layout=` | Stable (Phase S1 — dump schema **10**) |
| `ui.Input` | Stable (Phase S2 — dump schema **13**; form → `@server`) |

Update this table when phases land and when RFCs/ADRs promote artifacts to Stable/Frozen. Breaking changes to Stable artifacts in `0.x` require an ADR and a dump schema version bump when applicable — see ADRs 001–004 under `docs/decisions/`.
