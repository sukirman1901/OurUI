# Roadmap

Product milestones (releases). Architecture RFCs live under `docs/rfcs/`. Capability generations are the north-star framing; lettered phases A–S are historical P0 / Phase S delivery.

## Capability generations

| Generation | Proof | Status |
|---|---|---|
| **1 — Language infrastructure** | Intent → SG → IIR → LTR → RTR → running app | Done |
| **2 — Semantic presentation** | Presentation Graph + Design System → Resolved Design | Done (`0.2.1`, dump schema 12) |
| **3 — Host** | Host consumes `RTR + Resolved Design` via **Host Contract** | Done (`0.3.0`) |

```text
Gen 1–3 complete. Phase S1–S6 language surface shipped (ourui 0.4.0, dump schema 21).
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

ADRs 005–007 record intent+emit+escape. Phase S language arc is complete at **0.4.0**.

## Next (optional / out of language scope)

- App-layer: Redis share, auth, billing, tables
- Host: PDF / native emitters on the same Host Contract
- Design System packs beyond `ourui-default`
- Published docs site (in-repo `docs/user/` is the Stable guide today)

See [VISION.md](../VISION.md) and [SPEC_STATUS.md](../SPEC_STATUS.md).
