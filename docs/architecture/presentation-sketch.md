# Presentation architecture (sketch)

**Status:** Draft pointer — normative decisions live in RFCs.

```text
Compiler → Presentation Graph (RFC-001)
                +
         Design System pack (RFC-002)
                ↓
         Resolved Design
                ↓
         Host Contract (RFC-003)
                ↓
         Web / PDF / Native …
```

**Generation 3 bottleneck:** Host must consume `RTR + Resolved Design`.  
CSS AST (if any) is a web-host implementation detail, not the Gen-3 gate.

Today: dump includes `presentation_graph` + `resolved_design`.  
Spike B (`0.2.2`): web emit reads Resolved Design for pack vars + button/link node CSS.  
Remaining for `0.3.0`: finish contract-primary path (Theme/`DEFAULT_*` no longer emit authority).

See:

- [RFC-001](../rfcs/RFC-001-presentation-system.md) Accepted + Implemented  
- [RFC-002](../rfcs/RFC-002-design-system.md) Accepted + Implemented  
- [RFC-003](../rfcs/RFC-003-host-emit.md) Draft — Host Contract  
- [Spike A/B/C](../rfcs/spikes/2026-07-18-presentation-abc.md)
