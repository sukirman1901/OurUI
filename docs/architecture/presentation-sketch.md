# Presentation architecture (sketch)

**Status:** Draft pointer — normative decisions live in RFCs.

```text
Compiler → Presentation Graph (RFC-001, Option A lowering)
                +
         Design System input (RFC-002)
                ↓
       Resolved Presentation
                ↓
         Host Emit (RFC-003 / ourui-web)
```

Provisional 0.1.x Theme + `_BASE_CSS` remains until RFC-002/003 migrate web emit.

See:

- [RFC-001](../rfcs/RFC-001-presentation-system.md)  
- [RFC-002 stub](../rfcs/RFC-002-design-system.md)  
- [RFC-003 stub](../rfcs/RFC-003-host-emit.md)  
- [Spike A/B/C](../rfcs/spikes/2026-07-18-presentation-abc.md)
