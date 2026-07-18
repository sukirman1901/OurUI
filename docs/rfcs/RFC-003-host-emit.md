# RFC-003: Host Emit (stub)

**Status:** Stub  
**Depends on:** RFC-001 Accepted; RFC-002 for Resolved Presentation  

## Intent

Define how **hosts** consume **Resolved Presentation** (+ RTR / Layout outputs) to produce concrete media.

## Host packages (sketch)

| Package | Output |
|---------|--------|
| `ourui-web` | HTML, CSS AST → CSS, JS, assets, hydration |
| `ourui-pdf` | PDF styling / layout (later) |
| `ourui-native` | Platform modifiers (later) |

## Rules

- Web HTML emitter must **not** own design-token tables.  
- CSS AST is a **web-host** artifact, not part of Presentation System core.  
- Presentation Graph remains host-neutral.

## Migration

Retire provisional `_BASE_CSS` / Theme→CSS shortcuts in favor of Resolved Presentation → CSS AST once RFC-002 lands.
