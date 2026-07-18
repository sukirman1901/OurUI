# Architecture Decision Records

See [RFC_PROCESS.md](../../RFC_PROCESS.md) for when to write an ADR vs an RFC.

ADRs record local or historical choices. RFCs change LOCKED architecture or vocabulary.

**Focus now:** package = **utilities** (ADR-013). `ui.Theme` = thin brand sheet (ADR-004, narrowed by ADR-013). Do not grow Stable `ui.*` with composed patterns while foundation is incomplete (ADR-014). See [VISION.md](../../VISION.md).

| ADR | Title |
|---|---|
| [ADR-001](ADR-001-p0-spec-stable.md) | Promote P0 specs to Stable |
| [ADR-002](ADR-002-prod-session-runtime.md) | Single-process prod serve + session State |
| [ADR-003](ADR-003-file-multiworker-sessions.md) | File-backed multi-worker sessions |
| [ADR-004](ADR-004-design-tokens.md) | Theme roles (`--ourui-*`) — thin sheet; narrowed by ADR-013 |
| [ADR-005](ADR-005-intent-emit-escape.md) | Presentation: intent + emit + escape — **S1–S6 Done (`0.4.0`)** |
| [ADR-006](ADR-006-chrome-nav-placement.md) | Chrome: `ui.Nav` + `placement=` → CSS position |
| [ADR-007](ADR-007-site-structure-stack.md) | Full site stack — **Implemented (`0.4.0`)** |
| [ADR-008](ADR-008-form-dialog-toast.md) | Form / Dialog / Toast (Phase T) |
| [ADR-009](ADR-009-diagnostics-derived.md) | Diagnostics + Derived Draft (Phase V) |
| [ADR-010](ADR-010-show-when-dynamic-list.md) | Show / When + dynamic List/Table |
| [ADR-011](ADR-011-pack-versioning-check-profile.md) | Density + `ourui check` profiles (historical pack API superseded) |
| [ADR-012](ADR-012-motion-vocabulary.md) | Motion vocabulary `family.pattern` (M0–M3; schema **30**) |
| [ADR-013](ADR-013-style-intent-catalog.md) | Style Intent Catalog — **foundation** (utilities) |
| [ADR-014](ADR-014-language-primitives-vs-kit.md) | Primitives first — no composed patterns in language yet |
