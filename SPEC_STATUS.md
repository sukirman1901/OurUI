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
**Phase S2–S6** (`v0.4.x`, dump schema **21**): form controls through Canvas + polish — **Stable**.  
**Phase T–W → 1.0**: language freeze — schema **25 Frozen**.  
**Enterprise E1–E5**: screen completeness through trust — schemas **26–27**.  
**Security (1.6.0)**: CSRF, session gate, CSP nonce, rate limit, attestation `sha256` — schema **28**.

See [roadmap.md](docs/roadmap.md).

### Capability generations

| Generation | Status |
|---|---|
| 1 — Language infrastructure | Done |
| 2 — Semantic presentation (PG + DS → Resolved Design) | Done (`0.2.1`) |
| 3 — Host (`RTR + Resolved Design` via Host Contract) | Done (`0.3.0`) |
| Phase S language surface (S1–S6) | Done (`0.4.x`, schema **21**) |
| Phase T–W → 1.0 freeze | Done (`1.0.0`, schema **25 Frozen**) |
| Enterprise E1 screen completeness | Done (`1.1.0`, schema **26**) |
| Enterprise E2–E5 (pack/density/check, operate, kit, trust) | Done (`1.5.0`, schema **27**) |
| Security hardening (CSRF, session gate, nonce, attest hash) | Done (`1.6.0`, schema **28**) |

| Area | Status |
|---|---|
| Vision | Stable |
| Design Principles | Stable |
| Invariants + LOCKED + vocabulary | Stable |
| Compilation Architecture | Stable |
| RFC Process | Stable |
| Language Spec | Stable → **Frozen** at `1.0` (T–V surfaces included) |
| Semantic Graph / DependencyGraph / IIR / LTR / RTR | Stable (`ourui dump`) |
| Presentation Graph | Stable (RFC-001) |
| Resolved Design | Stable (RFC-002 — required emit input) |
| Host Contract | **Frozen** at `1.0` (RFC-003) |
| HTML / CSS / JS emit | Stable |
| Design tokens (`ui.Theme`) | Stable — color, type, space, elevation |
| `ourui serve` / State / `@server` / HMR / routing / LSP | Stable |
| `ourui check` / structured diagnostics | Stable (Phase V) |
| Runtime (prod + multi-worker file store) | Stable |
| Package (`ourui` **1.7.1**) | Dump schema **29** (additive; 25 Frozen baseline at 1.0) |
| Named packs + recipes | Stable (**1.7.0**) |
| `ui.Show` / `ui.When` | Stable (Enterprise E1) |
| Dynamic `List`/`Table` (`items=`/`rows=` State) | Stable (Enterprise E1) |
| Pack versioning + density | Stable (Enterprise E2) |
| `ourui check --profile enterprise` | Stable (Enterprise E2) |
| Dump `attestation` + emit CSP baseline | Stable (Enterprise E5; `sha256` in **1.6.0**) |
| Prod CSRF / session gate / CSP nonce / rate limit | Stable (**1.6.0**) |
| Auth gateway example | Stable (app-layer; `examples/enterprise/gateway/`) |
| PDF second host (RFC-004) | Draft (deferred) |
| `Derived` | Draft (Phase V) |
| `ui.Input` / `Select` / `Toggle` / `Slider` / `textarea` | Stable (S2 + 0.4.1) |
| `ui.Nav` | Stable (S3a) |
| Type/space/elevation tokens + `ui.ThemeToggle` | Stable (S3) |
| `ui.Footer` + Hero/Section `pad=` | Stable (S3b) |
| `gap=` / `align=` / `justify=` / `split-sidebar` | Stable (S4) |
| `motion=` presets | Stable (S4m) |
| `ui.Canvas` / `ui.Frame` | Stable (S5 / 0.4.1) |
| Drawer / Menu / Image / Icon / Meta / Code / CopyButton / control states | Stable (S6) |
| `ui.Form` / `ui.Dialog` / `ui.Toast` | Stable (Phase T) |
| `ui.List` / `ui.Table` / `ui.Empty` / `ui.Spinner` / `ui.Alert` | Stable (Phase U) |
| `Derived` | Draft (Phase V) |
| Design System pack API (`ourui-default`) | Stable (Phase W seed) |

### Out of language scope (still)

Redis share backends, auth, billing — app concerns, not language phases.

Update this table when phases land. Breaking changes to **Frozen** dump schema in `1.x` require a major version (`2.0`) and ADR — see ADRs under `docs/decisions/`.
