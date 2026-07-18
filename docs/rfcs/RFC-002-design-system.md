# RFC-002: Design System (stub)

**Status:** Stub  
**Depends on:** RFC-001 Accepted  

## Intent

Define the **Design System** as **compiler input**: resources + rules (not a Compilation Flow stage).

Industry name **Design System** is kept (Material, Fluent, Polaris). Role:

> A set of resources and rules that map a **Presentation Graph** into values suitable for host emission (Resolved Presentation).

## Tentative contents

- Tokens / palettes  
- Typography, spacing, elevation, radius, density scales  
- Theme presets (`Material3`, `Corporate`, …)  
- Motion presets as design vocabulary  
- Font / icon packs as resources  

## Resolution bias (to validate later)

```text
Presentation Graph + Design System → Resolved Presentation → Host
```

## Non-goals (stub)

- Implementing Material inside the compiler  
- CSS AST (RFC-003)  
- Changing Presentation Graph production (RFC-001)

## Package sketch (later)

`ourui-theme/` or design-resources packs: `material/`, `fluent/`, `corporate/`.
