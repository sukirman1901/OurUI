# Presentation architecture (sketch)

**Status:** Draft pointer — normative decisions live in RFCs.

```text
Compiler → Presentation Graph (RFC-001)
                +
         Design System pack (RFC-002)
                ↓
         Resolved Design
                ↓
         Host Contract (RFC-003)  — RTR + Resolved Design (required)
                ↓
         Web / PDF / Native …
```

**Generation 3 Done (`0.3.0`):** web emit is contract-primary.  
**Phase S Done (`0.4.0`):** language surface through Canvas + polish (schema 21).  
`_BASE_CSS` is host-private chrome (layout). Design values come from Resolved Design.  
CSS AST (if any) remains an optional web-host detail (Step F).

See:

- [RFC-001](../rfcs/RFC-001-presentation-system.md) Accepted + Implemented  
- [RFC-002](../rfcs/RFC-002-design-system.md) Accepted + Implemented  
- [RFC-003](../rfcs/RFC-003-host-emit.md) Accepted + Implemented  
- [Spike A/B/C](../rfcs/spikes/2026-07-18-presentation-abc.md)
