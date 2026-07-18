# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`. Capability generations are the north-star framing; lettered phases A–S are historical P0 / Phase S delivery; **T→1.0** is the post–Phase S language arc.

## Capability generations

| Generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done (`0.2.1`, dump schema 12) |
| **3 — Host** | Host consumes `RTR + Resolved Design` via **Host Contract** | Done (`0.3.0`) |

```text
Gen 1–3 complete. Phase S1–S6 shipped (0.4.x, schema 21).
Phase T–W shipped; dump schema 25 Frozen at ourui 1.0.0.
```

## Historical phases (P0 → S)

| Phase | Deliverable | Status |
|---|---|---|
| **A–R** | Docs freeze through first PyPI package | Done |
| **S1** | `ui.Link` + `ui.Shell` / `layout=` (schema 10, `0.1.2`) | Done |
| **Presentation / Design / Host R&D** | RFC-001 → RFC-003; contract-primary emit (`0.3.0`) | Done |
| **S2** | Form controls → `@server` (schema 14, `0.3.2`) | Done |
| **S3a** | `ui.Nav` + `placement=` + `tone=` (schema 15, `0.3.3`) | Done |
| **S3–S6** | Tokens, Footer, layout, motion, Canvas, polish (schema 21, `0.4.0`) | Done |
| **0.4.1** | `textarea` Input + `ui.Frame` preview escape | Done |

ADRs 005–007 record intent+emit+escape. Phase S language arc closed at **0.4.0**.

## Post–Phase S (language arc → 1.0)

| Phase | Deliverable | Target | Schema | Status |
|---|---|---|---|---|
| **T** | Form / Dialog / Toast + field error standardization | `0.5.0` → `1.0` | 22→25 | **Done** |
| **U** | List / Table / Empty / Spinner / Alert | `0.6.0` → `1.0` | 23→25 | **Done** |
| **V** | Structured diagnostics, `ourui check`, LSP diagnostics, Derived (Draft) | `0.7.0` → `1.0` | 24→25 | **Done** |
| **W** | Trusted Publishing, deploy docs, design packs | `0.8–0.9` → `1.0` | as needed | **Done** |
| **1.0** | Freeze bar (Stable surfaces + dump schema Frozen for 1.0.x) | `1.0.0` | **25 Frozen** | **Done** |

Principles: intent + emit + escape ([ADR-005](decisions/ADR-005-intent-emit-escape.md)); Host Contract ([RFC-003](rfcs/RFC-003-host-emit.md)); playground dogfoods language — language does not depend on demo chrome.

### Phase T — Form & overlay chrome

- `ui.Form(..., on_submit=)` — collect fields on submit / Enter
- Field `invalid=` + helper text (`aria-invalid`)
- `ui.Dialog(title=, open=, actions=)` — modal overlay
- `ui.Toast` — ephemeral messages via State

### Phase U — Data & list patterns

- `ui.List` / `ui.Table` (semantic, not spreadsheet)
- `ui.Empty` / `ui.Spinner` / `ui.Alert`
- Document `@server` + State async patterns (no new FE framework)

### Phase V — Compiler & author UX

- Structured diagnostics (`path` + span)
- `ourui check` CLI
- LSP diagnostics
- `Derived` state (Draft → Stable with ADR)

### Phase W — Ship maturity

- GitHub Trusted Publishing → PyPI
- Deploy recipe (Docker / static+RPC)
- Design pack API growth (`ourui-default`)

### 1.0 freeze criteria

1. Phases T–V implemented and documented Stable
2. Dump schema Frozen for `1.0.x` (breaking → `2.0`)
3. LANGUAGE_SPEC + Host Contract Frozen where applicable
4. Non-goals restated: no Monaco-in-language, no auth-in-language

## Out of language scope (unchanged)

Redis share, auth, billing — app concerns. Optional PDF/native hosts only via Host Contract + RFC.

See [VISION.md](../VISION.md) and [SPEC_STATUS.md](../SPEC_STATUS.md).
