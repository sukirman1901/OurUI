# Presentation architecture (sketch)

**Status:** Draft pointer — normative decisions live in RFCs.

```text
Compiler → Presentation Graph (RFC-001, Option A lowering)
                +
         Design System pack (RFC-002, ourui-default)
                ↓
         Resolved Design (dump schema 12)
                ↓
         Host Emit (RFC-003 — not yet wired)
```

Today: dump includes `presentation_graph` + `resolved_design`.  
Provisional emit still uses Theme + `_BASE_CSS` until RFC-003 wires `RTR + Resolved Design → HTML/CSS`.

See:

- [RFC-001](../rfcs/RFC-001-presentation-system.md) Accepted + Implemented  
- [RFC-002](../rfcs/RFC-002-design-system.md) Accepted + Implemented  
- [RFC-003 stub](../rfcs/RFC-003-host-emit.md)  
- [Spike A/B/C](../rfcs/spikes/2026-07-18-presentation-abc.md)
