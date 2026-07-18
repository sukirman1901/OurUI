# Presentation architecture (sketch)

**Status:** Draft pointer — normative decisions live in RFCs.

```text
Compiler → Presentation Graph (RFC-001)
                +
         Theme defaults + overrides → Resolved Design (RFC-002)
                ↓
         Host Contract (RFC-003)  — RTR + Resolved Design (required)
                ↓
         Web / PDF / Native …
```

Theme seed: `ourui.theme` (`DEFAULT_LIGHT` / `DEFAULT_DARK`). Craft depth: style intents (ADR-013), not Theme alone.

**Package `1.11.1`**, dump schema **30** (language/IR Frozen at **25**).  
`_BASE_CSS` is host-private chrome. Design values come from Resolved Design.  
CSS AST (if any) remains an optional web-host detail.

See:

- [RFC-001](../rfcs/RFC-001-presentation-system.md) Accepted + Implemented  
- [RFC-002](../rfcs/RFC-002-design-system.md) Accepted + Implemented  
- [RFC-003](../rfcs/RFC-003-host-emit.md) Accepted + Implemented  
- [Spike A/B/C](../rfcs/spikes/2026-07-18-presentation-abc.md)
