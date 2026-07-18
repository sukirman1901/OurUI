# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`. Capability generations are the north-star framing; lettered phases A–S / T→1.0 are historical; **E1–E5** is the post-1.0 **enterprise** arc.

## Capability generations

| Generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done (`0.2.1`, dump schema 12) |
| **3 — Host** | Host consumes `RTR + Resolved Design` via **Host Contract** | Done (`0.3.0`) |

```text
Gen 1–3 + Phase S + T–W complete at ourui 1.0.x (schema 25 Frozen baseline).
Enterprise arc E1–E5 complete at ourui 1.5.0 (additive dump schema 27).
Security hardening complete at ourui 1.6.0 (additive dump schema 28).
```

## Historical (done)

| Phase | Deliverable | Status |
|---|---|---|
| **A–S / T–W / 1.0** | Language infra through Form/List/diagnostics + freeze | Done (`1.0.x`, schema **25**) |
| **1.0.1** | Default visual quality (zinc/ink pack) | Done |

## Enterprise arc (post-1.0)

Enterprise = org-scale packs + complete product screens + operable deploy + governance — **not** auth/ORM inside `ui.*`. See ADRs; kit templates keep SSO/DB at app-layer.

| Phase | Deliverable | Target | Schema | Status |
|---|---|---|---|---|
| **E1** | Screen completeness: `Show`/`When`, dynamic List/Table, form depth, CRUD reference | `1.1.0` | **26** | **Done** |
| **E2** | Org design system: pack versioning, density, a11y in `ourui check` | `1.2`–`1.5` | **27** | **Done** |
| **E3** | Operate: CI emit artifact, Docker/K8s gold path | `1.3`–`1.5` | **27** | **Done** |
| **E4** | Enterprise Kit 1.0 (clone → brand → deploy ≤5 days) | `1.4`–`1.5` | **27** | **Done** |
| **E5** | Trust: CSP defaults, SBOM, IR attestation; optional PDF host (RFC Draft) | `1.5.0` | **27** | **Done** |
| **S1** | Host security: CSRF, session gate, CSP nonce, rate limit, attest `sha256`, gateway | `1.6.0` | **28** | **Done** |

### E1 — Screen completeness (`1.1.0`)

- `ui.Show(show=State, …)` — visibility twin of Dialog `open=`
- `ui.When(show=, then=, else_=)` — both branches in DOM; host toggles
- `ui.List(items=State)` / `ui.Table(rows=State)` — host rebuilds from JSON
- Form depth: documented error/`disabled`/`loading` patterns
- Reference: `examples/enterprise/crud_app.py`

### E2 — Org design system (`1.5.0`)

- Versioned named packs (`pack_version` on Resolved Design) + density recipes
- `ui.Theme(density="compact"|"comfortable")` → `ourui-density-compact`
- `ourui check --profile enterprise` (+ `--strict`); ADR-011

### E3 — Operate (`1.5.0`)

- CI workflow emit + Docker/Compose/K8s recipes under `deploy/`

### E4 — Enterprise Kit (`1.5.0`)

- Pack + Admin CRUD + Settings + Audit UI + AI console shells
- Auth/DB as **templates** (FastAPI+OIDC stub), not language

### E5 — Trust surface (`1.5.0`)

- CSP-friendly emit defaults (`data-ourui-csp="1"`), SBOM note, dump attestation
- Optional second host (PDF) via Host Contract — [RFC-004](rfcs/RFC-004-second-host-pdf.md) Draft (deferred)

## Out of language scope (unchanged)

Redis share, auth, billing, ORM — app concerns. No React/Tailwind clone; no Monaco-in-language.

See [VISION.md](../VISION.md) and [SPEC_STATUS.md](../SPEC_STATUS.md).
