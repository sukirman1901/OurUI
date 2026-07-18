# Spec Status

Status ladder:

| Status | Meaning |
|---|---|
| **Experimental** | May change freely; not relied upon |
| **Draft** | Intended direction; expect revisions |
| **Stable** | Safe to depend on within a major version |
| **Frozen** | Must not change until the next major version |

## Current focus (`1.11.0`)

**L3 complete:** Style Intent Catalog depth (ADR-013) — high-ROI utilities, responsive dicts, `Theme(css=)`, host-chrome slim, long-tail props. Catalog matrix **1.5.0**.

| Priority | What |
|---|---|
| **Next** | Dogfood (`examples/landing/`) + niche **C** only when needed; optional hover/focus intent depth |
| Supporting | Thin theme roles (`ui.Theme`), thin primitives, Host Contract, serve/check |
| **Not now** | Composed UI patterns inside Stable `ui.*` |

Dump schema **25** remains **Frozen** for language/IR breaking changes in `1.x`. Current dump schema **30** (additive). Package **1.11.0**.

See [VISION.md](VISION.md) · [roadmap.md](docs/roadmap.md).

## Capability generations

| Generation | Status |
|---|---|
| 1 — Language infrastructure | Done |
| 2 — Presentation Graph + Resolved Design | Done (`0.2.1`) |
| 3 — Host Contract (RTR + Resolved Design → emit) | Done (`0.3.0`) |
| Phase S language surface (S1–S6) | Done (`0.4.x`, schema **21**) |
| Phase T–W → 1.0 freeze | Done (`1.0.0`, schema **25 Frozen**) |
| Screen/runtime completeness (Show/When, density, check, trust) | Done (`1.1`–`1.5`, schemas **26–27**) |
| Security hardening (CSRF, session gate, nonce, attest hash) | Done (`1.6.0`, schema **28**) |
| Style Intent Catalog (foundation) | **L3 Done** (`1.11.0`, catalog **1.5.0**, schema **30**) |

## Spec surfaces

| Area | Status |
|---|---|
| Vision / Design Principles | Stable — foundation = utilities |
| Invariants + LOCKED + vocabulary | Stable |
| Compilation Architecture | Stable |
| RFC Process | Stable |
| Language Spec | Stable → **Frozen** at `1.0` |
| Semantic Graph / DependencyGraph / IIR / LTR / RTR | Stable (`ourui dump`) |
| Presentation Graph | Stable (RFC-001) |
| Resolved Design | Stable (RFC-002 — required emit input; seeded from `ourui.theme`) |
| Host Contract | **Frozen** at `1.0` (RFC-003) |
| HTML / CSS / JS emit | Stable |
| **Style Intent Catalog** (ADR-013) | Stable · **L3 shipped** (niche **C** remain) |
| **`ui.Theme`** (roles + density + `page=` + `css=`) | Stable — thin brand sheet + author CSS escape |
| Thin primitives (`Page`, `Nav`, `Button`, forms, …) | Stable — emit mapping |
| `motion=` (`family.pattern`) | Stable (146 patterns, catalog **1.2.0**) |
| `ourui serve` / State / `@server` / HMR / routing / LSP | Stable |
| `ourui check` (`default` \| `a11y`, optional `--strict`) | Stable |
| Dump `attestation` + emit CSP baseline | Stable (`sha256` since **1.6.0**) |
| Prod CSRF / session gate / CSP nonce / rate limit | Stable (**1.6.0**) |
| Package (`ourui` **1.11.0**) | Dump schema **30** |
| `Derived` | Draft (Phase V) |
| PDF second host (RFC-004) | Draft (deferred) |
| Auth gateway example | App-layer only (`examples/gateway/`) — not language |

### Language surface (Stable kinds — summary)

Forms, Nav/Footer/Meta, layout intents, Show/When, List/Table, Form/Dialog/Toast, Canvas/Frame escapes, polish (Image/Icon/Code/Menu/…). Full list: [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md).

### Out of language scope

- Redis / distributed sessions, auth, billing, ORM — app concerns
- Composed section patterns / component marketplaces inside Stable `ui.*`
- Tailwind **class-string** authoring (`class="aspect-video"`)

Update this table when phases land. Breaking changes to **Frozen** dump schema in `1.x` require a major version (`2.0`) and ADR — see ADRs under `docs/decisions/`.
