# RFC-001: Presentation System

**Status:** Accepted + Implemented (dump `presentation_graph`, schema 11, package `0.2.0`)  
**Track:** Presentation R&D  
**Relates:** ADR-005, ADR-007; RFC-002 (Design System); RFC-003 (Host Emit)

## Motivation

OurUI 0.1.x has a working compiler and provisional HTML/CSS emit (`ui.Theme`, `_BASE_CSS`). The Plasma dogfood showed that **Presentation** — not more compiler plumbing — is the main gap. Presentation must stay **host-neutral** and must not absorb Design System tokens or CSS.

## Scope (this RFC only)

In scope:

- **Presentation Intent** (from authoring / IIR Presentation Domain)
- **Presentation Graph** (dumpable, host-neutral)
- How the Graph is produced: options **A / B / C** (below)

Out of scope (later RFCs):

- Design tokens, theme presets, type/spacing scales → **RFC-002**
- CSS AST, HTML/JS bundling, PDF/native → **RFC-003**
- New chrome widgets (`ui.Nav`, etc.) until Graph + resolve path exist

## Artifacts (named; pass order not locked)

| Artifact | Meaning |
|----------|---------|
| Presentation Intent | Semantic presentation meaning on nodes (e.g. `tone=primary`, layout role) |
| Presentation Graph | Host-neutral graph of presentation structure / roles |

Transforms between Intent and Graph may be refined in implementation; only the **artifacts** are required.

## Production options (Q1)

| Option | Path | Nature |
|--------|------|--------|
| **A** | IIR → Presentation Lowering → Presentation Graph | Derived artifact (like LTR) |
| **B** | IIR → **PIR** → Presentation Graph | Peer IR letter |
| **C** | SG/IIR → Presentation **Analysis** → Presentation Graph | Analysis View–like index |

## Decision (post-spike)

**Choose Option A** for 0.2: Presentation Graph is produced by a **Presentation Lowering** pass from IIR (presentation-domain attrs + kind roles), dumpable alongside LTR/RTR.

**Defer Option B (PIR)** unless multi-host or tooling later proves a peer letter is required.  
**Reject Option C as the primary path** for now: Analysis Views must not become a silent second Flow; if indexing is needed later, it can derive *from* the Graph.

Evidence: [spikes/2026-07-18-presentation-abc.md](spikes/2026-07-18-presentation-abc.md).

## Boundary

```text
Presentation System:  Intent → Graph
Design System:        input resources + rules (RFC-002)
Host:                 Resolved Presentation → concrete medium (RFC-003)
```

```text
Presentation Graph + Design System → Resolved Presentation → Host
```

(Resolution bias for RFC-002; not implemented in this RFC.)

## Provisional 0.1.x

Current Theme + `_BASE_CSS` remain a **provisional web path** until RFC-002/003 migrate emit to consume Resolved Presentation.

## Implementation plan (Accepted → code)

1. Add `presentation_graph` to `ourui dump` (schema bump).  
2. Lower from IIR presentation attrs / kinds (Option A).  
3. Keep HTML emit unchanged initially (still provisional).  
4. Open full RFC-002 after Graph dumps stably.

## Vocabulary

New terms (official once Implemented): **Presentation Intent**, **Presentation Graph**, **Presentation Lowering**.

## References

- [ADR-005](../decisions/ADR-005-intent-emit-escape.md)  
- [ADR-007](../decisions/ADR-007-site-structure-stack.md)  
- [RFC_PROCESS.md](../../RFC_PROCESS.md)
