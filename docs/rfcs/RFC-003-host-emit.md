# RFC-003: Host Contract

**Status:** Accepted + Implemented (`0.3.0` — emit contract-primary)  
**Depends on:** [RFC-001](RFC-001-presentation-system.md) Accepted; [RFC-002](RFC-002-design-system.md) Accepted  
**Track:** Generation 3 — Host  

## Motivation

Generation 1 proved a UI language can compile and run.  
Generation 2 proved presentation meaning can be separated from design knowledge:

```text
Presentation Graph  +  Design System  →  Resolved Design
```

Generation 3 proves **Host** consumes them via a clean contract:

```text
RTR  +  Resolved Design  →  Host Emit  →  HTML / CSS / JS
```

## Center of this RFC (locked)

**Not** “build a CSS AST first.”

**Yes** — **Host Contract**:

```text
Host
  Input:   RTR  +  Resolved Design   (both required)
  Output:  medium-specific product (HTML+CSS+JS today; PDF / native later)
```

CSS AST (if any) is an **implementation detail of the web host**.

## Generational context

| Generation | Proof | Status |
|------------|-------|--------|
| **1** Language infrastructure | Intent → … → running app | Done |
| **2** Semantic presentation | PG + DS → Resolved Design | Done (`0.2.1`) |
| **3** Host | Host Contract → web emit | **Done (`0.3.0`)** |

## Host Contract — v0 (Implemented)

### Inputs (required)

| Input | Role |
|-------|------|
| **RTR** | Structure, text, events, binds, host kinds / attributes |
| **Resolved Design** | Per-node concrete values + mode/pack token maps |

Calling `emit_css` / `emit_html_document` / `emit_bundle` without `resolved_design` raises `TypeError`.

### Outputs (web host)

| Output | How |
|--------|-----|
| HTML | Structure + events from RTR (`data-ourui-id`, hooks) |
| CSS | Pack vars from `resolved_design.tokens` + per-node button/link rules; **host-private chrome** in `_BASE_CSS` (layout only — not Design System) |
| JS | Events / binds from RTR |

### Non-goals (deferred)

- Material / Fluent packs  
- Plasma visual parity  
- New chrome (`ui.Nav`)  
- CSS AST / package split `ourui-web` (optional later — Step F)

## Rules

1. Emit **requires** Resolved Design; Theme/`DEFAULT_*` are **not** emit authority (they seed the Design System pack only).  
2. Resolved Design stays host-neutral literals; Host may emit CSS variables.  
3. Presentation Graph is not a Host emit input.  
4. `_BASE_CSS` = host-private chrome (layout/structure).  

## Migration plan

| Step | Deliverable | Status |
|------|-------------|--------|
| **A** | Accept Host Contract text | Done |
| **B** | Spike: emit reads `resolved_design` | Done (`0.2.2`) |
| **C** | Remove emit fallbacks inventing tones from `DEFAULT_*` | **Done (`0.3.0`)** |
| **D** | Document `_BASE_CSS` as host-private chrome | **Done** |
| **E** | Release **0.3.0** contract-primary | **Done** |
| **F** | Optional: CSS AST / `ourui-web` | Later |

## Acceptance criteria

- [x] Host Contract vocabulary frozen  
- [x] CSS AST is optional, not Gen-3 gate  
- [x] Spike B + contract-primary emit  
- [x] No Material / Nav / Plasma on the critical path  

## Implementation notes

- Pipeline always passes `resolved_design` into emit.  
- Dump: `emit.host_contract` + `emit.host_contract_primary` (schema 12).  
- `theme.py` remains pack seed for `ourui.design.resolve` / `default_pack`.  

## References

- [RFC-001](RFC-001-presentation-system.md)  
- [RFC-002](RFC-002-design-system.md)  
- [ADR-004](../decisions/ADR-004-design-tokens.md)  
- [ADR-005](../decisions/ADR-005-intent-emit-escape.md)  
- `packages/ourui/ourui/emit/html.py`
