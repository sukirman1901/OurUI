# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`.

## Current focus

**Foundation L3 shipped** (`1.11.0`). Catalog **1.11.0** — **0 C**. Dogfood deferred.

| Layer | Status |
|---|---|
| Compiler spine | Shipped |
| **Utility catalog** | **L3 Done** (catalog **1.11.0**, **0 C**) |
| `ui.Theme` (thin roles + density + `page=` + `css=`) | Shipped — not craft depth |
| Thin primitives + host emit | Shipped |
| Examples (`tutorial/`, `landing/`) | Dogfood next |

See [VISION.md](../VISION.md) · [SPEC_STATUS.md](../SPEC_STATUS.md).

## Active — language utilities

| Phase | Deliverable | Package | Status |
|---|---|---|---|
| **L1** | Style Intent Catalog skeleton — scales + props + emit utilities | `1.9.0` | Done |
| **L2** | Primitives boundary; promote high-use C→A | `1.9.1` | Done |
| **L3** | Fill catalog depth — see [tailwind-gap.md](architecture/tailwind-gap.md) | `1.11.0` | **Done** |

## Shipped (summary)

| Milestone | What | Package |
|---|---|---|
| Gen 1–3 | Language → Resolved Design → Host Contract | `0.2`–`0.3` |
| Phase S / T–W | Forms through Canvas + polish; language freeze | `0.4`–`1.0` (schema **25 Frozen**) |
| Screen + runtime | Show/When, density, `ourui check --profile a11y`, trust/CSP | `1.1`–`1.5` |
| Security | CSRF, session gate, CSP nonce, rate limit, attest `sha256` | `1.6.0` |
| Motion | `motion=family.pattern` (146 Stable) | `1.8.x` |
| Theme measure | `Theme(page=)`, broader `aspect=` | `1.10.0` |
| **Style Intent L3** | ring/divide/space/scroll/gradient/sr/caret, responsive dicts, `Theme(css=)`, host-chrome slim, long-tail | `1.11.0` |

Detail and older release notes: [CHANGELOG.md](../CHANGELOG.md).

## Out of language scope

No Redis, auth, billing, ORM — app concerns. No React clone. No Tailwind **class-string** authoring. No composed section marketplace inside Stable `ui.*` ([ADR-014](decisions/ADR-014-language-primitives-vs-kit.md)).
