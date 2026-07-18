# RFC-003: Host Emit (stub)

**Status:** Stub → next Draft  
**Depends on:** RFC-001 Accepted; RFC-002 Accepted (`resolved_design` in dump)  

## Intent

Define how **hosts** consume **Resolved Design** (+ RTR / Layout outputs) to produce concrete media.

## Host packages (sketch)

| Package | Output |
|---------|--------|
| `ourui-web` | HTML, CSS AST → CSS, JS, assets, hydration |
| `ourui-pdf` | PDF styling / layout (later) |
| `ourui-native` | Platform modifiers (later) |

## Rules

- Web HTML emitter must **not** own design-token tables.  
- CSS AST is a **web-host** artifact, not part of Presentation System core.  
- Presentation Graph and Resolved Design remain host-neutral.

## Migration

Retire provisional `_BASE_CSS` / Theme→CSS shortcuts in favor of `RTR + Resolved Design → CSS AST` once this RFC is Implemented.
