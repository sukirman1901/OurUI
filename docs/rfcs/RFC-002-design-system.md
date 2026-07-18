# RFC-002: Design System → Resolved Design

**Status:** Accepted + Implemented (dump `resolved_design`, schema 12)  
**Depends on:** [RFC-001](RFC-001-presentation-system.md) Accepted  
**Relates:** [RFC-003](RFC-003-host-emit.md) (Host consumes Resolved Design)  
**Track:** Design System R&D (Generation 2)  
**Package:** `0.2.1`

## Motivation

Generation 1 proved a UI language can compile and run. Generation 2 must prove **high-quality presentation without host lock-in**.

Today emit still does:

```text
RTR + Theme tables + _BASE_CSS  →  HTML/CSS
```

The missing step is:

```text
Presentation Graph  +  Design System  →  Resolved Design  →  Host
```

Until **Resolved Design** exists, visual quality depends on provisional `_BASE_CSS`, and Design System knowledge is wrongly owned by the HTML emitter (`theme.py` + `emit/html.py`).

## Vocabulary (frozen for this RFC)

| Term | Meaning |
|------|---------|
| **Design System** | Compiler **input**: resources + rules (not a Compilation Flow stage). Industry name kept (Material, Fluent, …). |
| **Design System pack** | A concrete bundle (default OurUI pack, later Material3, Corporate, …). |
| **Resolved Design** | Dumpable, host-neutral artifact: presentation nodes with **concrete resolved values** (colors, spacing, radius, type roles as values — still not CSS rules). |
| **Resolution** | Pure function: `(Presentation Graph, Design System pack, mode?) → Resolved Design`. |

Alias: earlier notes said “Resolved Presentation”; **Resolved Design** is the official name going forward.

## Role of Design System

Design System is a **knowledge base**, like fonts or localization packs:

```python
ui.Theme(preset="Material3")   # selects a pack — compiler does not invent Material
```

Compiler understands semantic roles (`tone=primary`).  
Design System maps roles → concrete values.  
Host maps Resolved Design → CSS / PDF / SwiftUI / …

## Resolution shape (locked bias)

**Option 1** (accepted as the Draft default):

```text
Presentation Graph  +  Design System pack
            ↓
      Resolved Design
            ↓
           Host   (RFC-003)
```

Rejected for Draft: treating Design System as a Flow stage after an already-resolved graph.

## Resolved Design — artifact sketch

Dump key: `resolved_design` (schema version bump when Implemented).

```json
{
  "pack": "ourui-default",
  "mode": "light",
  "nodes": {
    "n0003": {
      "id": "n0003",
      "kind": "Button",
      "role": "button",
      "tone": "primary",
      "resolved": {
        "fill": "#1a5f4a",
        "fg": "#f5faf8",
        "radius": "0.5rem",
        "pad_block": "0.5rem",
        "pad_inline": "0.75rem"
      }
    }
  },
  "tokens": { "light": { "...": "..." }, "dark": { "...": "..." } }
}
```

Rules:

- Values are **medium-agnostic literals** (hex, rem, role names) — not `var(--ourui-*)` and not CSS selectors.  
- Host (RFC-003) may turn literals into CSS variables, PDF colors, etc.  
- Nodes without tones still appear with structural defaults from the pack (spacing/radius).

## Design System pack — contents (v0)

Minimum pack for first spike (migrate from today’s `theme.py` defaults):

| Resource | Purpose |
|----------|---------|
| Color roles | `primary`, `primary_fg`, `muted`, … |
| Space scale | `space_sm`, `space_md`, … |
| Radius | `radius` |
| Mode maps | `light` / `dark` |

Later packs may add type scale, elevation, motion presets, fonts, icons — without changing Presentation Graph.

Authoring bridge (provisional → RFC-002):

- Today: `ui.Theme(primary=...)` merges into SG tokens.  
- Target: Theme selects/overrides a **pack**; Resolution reads pack + overrides; HTML emit stops importing token tables.

## Non-goals

- CSS AST / critical CSS (RFC-003)  
- Changing how Presentation Graph is produced (RFC-001)  
- Shipping Material/Fluent packs in the first spike (default OurUI pack only)  
- Making emit beautiful / Plasma-parity  
- New chrome (`ui.Nav`)  

## Spike plan (Draft → Accepted)

1. Extract current `DEFAULT_LIGHT` / `DEFAULT_DARK` as pack `ourui-default`.  
2. Implement `resolve(presentation_graph, pack, mode) → resolved_design`.  
3. Add `resolved_design` to `ourui dump` (schema **12**).  
4. **Do not** change HTML emit yet (still provisional) — proves artifact existence.  
5. Test: Button with `color=primary` gets resolved fill/fg from pack.  
6. Accept RFC-002 when dump is stable; RFC-003 then wires `RTR + Resolved Design → HTML`.

## Migration from provisional path

| Today | After RFC-002 Implemented | After RFC-003 |
|-------|---------------------------|---------------|
| `theme.py` owned by emit | Pack module / `ourui-theme` input | Emit reads Resolved Design only |
| `_BASE_CSS` hardcodes tones | Layout chrome CSS may remain host-private | Tone colors from Resolved Design |
| SPEC “tokens Stable” | Relabel pack path; emit provisional until 003 | Host path Stable |

## Acceptance criteria

- [x] RFC text reviewed  
- [x] Spike dump includes `resolved_design`  
- [x] Emit still independent of Resolved Design (documented) until RFC-003  
- [x] Vocabulary: Design System, Resolved Design, Resolution — frozen  

## Implementation checklist (post-Accept)

1. [x] Code: `ourui.design` + dump wiring  
2. [x] Schema 12 + tests + CHANGELOG  
3. [x] Update `SPEC_STATUS` / architecture sketch  
4. Open RFC-003 Draft for host consumption  

## References

- [RFC-001](RFC-001-presentation-system.md)  
- [RFC-003](RFC-003-host-emit.md)  
- [ADR-004](../decisions/ADR-004-design-tokens.md) (provisional token emit)  
- [ADR-005](../decisions/ADR-005-intent-emit-escape.md)  
- [theme.py](../../packages/ourui/ourui/theme.py) (current pack seed)
