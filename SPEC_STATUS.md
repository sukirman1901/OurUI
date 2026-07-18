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
**Phase N–O**: production / multi-worker serve **Stable**.  
**Phase P**: design tokens **Stable**.  
**Phase R–S1**: package + Link/Shell **Stable**.  
**RFC-001–003**: Presentation Graph, Resolved Design, Host Contract **Stable** / Implemented.  
**Phase S2–S6** (`v0.4.0`, dump schema **21**): form controls through Canvas + polish — **Stable**.

### Capability generations

| Generation | Status |
|---|---|
| 1 — Language infrastructure | Done |
| 2 — Semantic presentation (PG + DS → Resolved Design) | Done (`0.2.1`) |
| 3 — Host (`RTR + Resolved Design` via Host Contract) | Done (`0.3.0`) |
| Phase S language surface (S1–S6) | Done (`0.4.0`, schema **21**) |

| Area | Status |
|---|---|
| Vision | Stable |
| Design Principles | Stable |
| Invariants + LOCKED + vocabulary | Stable |
| Compilation Architecture | Stable |
| RFC Process | Stable |
| Language Spec | Stable (P0 + Phase S through S6) |
| Semantic Graph / DependencyGraph / IIR / LTR / RTR | Stable (`ourui dump`) |
| Presentation Graph | Stable (RFC-001) |
| Resolved Design | Stable (RFC-002 — required emit input) |
| Host Contract | Stable (RFC-003 — emit requires RTR + Resolved Design) |
| HTML / CSS / JS emit | Stable |
| Design tokens (`ui.Theme`) | Stable — color, type, space, elevation |
| `ourui serve` / State / `@server` / HMR / routing / LSP | Stable |
| Runtime (prod + multi-worker file store) | Stable |
| Package (`ourui` **0.4.0**) | Stable ([PyPI](https://pypi.org/project/ourui/)) |
| `ui.Link` / `Shell` / `layout=` | Stable (S1) |
| `ui.Input` / `Select` / `Toggle` / `Slider` | Stable (S2) |
| `ui.Nav` | Stable (S3a) |
| Type/space/elevation tokens + `ui.ThemeToggle` | Stable (S3) |
| `ui.Footer` + Hero/Section `pad=` | Stable (S3b) |
| `gap=` / `align=` / `justify=` / `split-sidebar` | Stable (S4) |
| `motion=` presets | Stable (S4m) |
| `ui.Canvas` (Plasma WebGL escape) | Stable (S5) |
| Drawer / Menu / Image / Icon / Meta / Code / CopyButton / control states | Stable (S6) |
| Design System pack API (`ourui-default`) | Draft (seeded from `theme.py`; packs may grow) |

### Out of language scope (still)

Redis share backends, auth, billing, data tables — app concerns, not Phase S.

Update this table when phases land. Breaking changes to Stable artifacts in `0.x` require an ADR and a dump schema version bump — see ADRs under `docs/decisions/`.
