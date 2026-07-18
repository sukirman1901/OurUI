# Spike: Presentation Graph production (A / B / C)

**Date:** 2026-07-18  
**RFC:** [RFC-001](../RFC-001-presentation-system.md)

## Method

Compared three shapes against the same IIR fixtures (`examples/tutorial/01_page.py`, `demo/app.py` mental model):

| Option | Prototype |
|--------|-----------|
| **A** | Lower IIR nodes → `presentation_graph.nodes[id] = { role, tone?, href?, shell_layout? }` |
| **B** | Insert PIR letter with generation+1 and full node copy before Graph |
| **C** | Treat Graph as Analysis View keyed off SG without a lowering provenance chain |

## Findings

1. **A** matches existing LTR/RTR discipline (immutable prior artifact, provenance `lowering:presentation`, dumpable). Lowest migration cost from 0.1.x.  
2. **B** adds vocabulary + dump schema weight without a second consumer yet (no PDF/native). Premature.  
3. **C** blurs Analysis Views vs Flow (INVARIANTS I8). Risky for contributors.

## Recommendation

**Accept Option A** for the first Implemented milestone. Revisit **B** if a host-neutral PIR is required by tooling/AI or a second host before CSS.

## Follow-up code

`ourui dump` includes `presentation_graph` via Presentation Lowering (schema version bump).
