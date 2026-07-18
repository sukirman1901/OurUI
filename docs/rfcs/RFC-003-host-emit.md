# RFC-003: Host Contract

**Status:** Accepted + Spike B Implemented (`0.2.2` — emit consumes Resolved Design)  
**Depends on:** [RFC-001](RFC-001-presentation-system.md) Accepted; [RFC-002](RFC-002-design-system.md) Accepted  
**Track:** Generation 3 — Host  
**Target release:** `0.3.0` when emit is contract-primary (DEFAULT token tables no longer emit source of truth)

## Motivation

Generation 1 proved a UI language can compile and run.  
Generation 2 proved presentation meaning can be separated from design knowledge:

```text
Presentation Graph  +  Design System  →  Resolved Design
```

Those artifacts exist in `ourui dump` (schema 12). Generation 3 proves **Host** consumes them:

```text
RTR  +  Resolved Design  →  Host Emit  →  HTML / CSS / JS
```

## Center of this RFC (locked)

**Not** “build a CSS AST first.”

**Yes** — **Host Contract**:

```text
Host
  Input:   RTR  +  Resolved Design
  Output:  medium-specific product (HTML+CSS+JS today; PDF / native later)
```

CSS AST (if any) is an **implementation detail of the web host**.

## Generational context

| Generation | Proof | Status |
|------------|-------|--------|
| **1** Language infrastructure | Intent → … → running app | Done |
| **2** Semantic presentation | PG + DS → Resolved Design | Done (`0.2.1`) |
| **3** Host | Host Contract → web emit | **In progress** (Spike B in `0.2.2`) |

## Host Contract — v0

### Inputs (required)

| Input | Role |
|-------|------|
| **RTR** | Structure, text, events, binds, host kinds / attributes |
| **Resolved Design** | Per-node concrete values + mode/pack token maps |

### Outputs (web host v0)

| Output | How (Spike B) |
|--------|----------------|
| HTML | Structure + events from RTR (`data-ourui-id`, hooks) |
| CSS | Pack vars from `resolved_design.tokens` + per-node rules from `resolved_design.nodes` for button/link; layout chrome remains host-private `_BASE_CSS` |
| JS | Events / binds from RTR (unchanged) |

### Non-goals for Contract v0

- Material / Fluent packs  
- Plasma visual parity  
- New chrome (`ui.Nav`)  
- Mandating CSS AST before Host can read Resolved Design  

## Rules

1. Emit prefers **Resolved Design** over Theme/`DEFAULT_*` as the design source for tones.  
2. Resolved Design stays host-neutral literals; Host may emit CSS variables.  
3. Presentation Graph is not a Host emit input (debug/compiler only).  
4. Chrome freeze continues until contract path is primary (`0.3.0`).  

## Migration plan

| Step | Deliverable | Status |
|------|-------------|--------|
| **A** | Accept Host Contract text | Done |
| **B** | Spike: emit reads `resolved_design` for Button/link tones | **Done (`0.2.2`)** |
| **C** | Remove remaining emit fallbacks that invent tones from `DEFAULT_*` alone | Next |
| **D** | Document `_BASE_CSS` as host-private chrome only | Partial |
| **E** | Release **0.3.0** when web emit is contract-primary | Planned |
| **F** | Optional: CSS AST / `ourui-web` package split | Later |

## Acceptance criteria

- [x] Host Contract vocabulary frozen  
- [x] CSS AST is optional, not Gen-3 gate  
- [x] Spike B: pipeline passes Resolved Design into emit; CSS includes per-node fills  
- [x] No Material / Nav / Plasma on the critical path  

## Implementation notes (Spike B)

- `emit_html` / `emit_bundle` pass `resolved_design` from the pipeline.  
- `emit_css(resolved_design=…)` seeds `--ourui-*` from RD tokens and appends `[data-ourui-id=…]` rules for button/link resolved values.  
- Dump `emit.host_contract: true` (schema remains 12).  

## References

- [RFC-001](RFC-001-presentation-system.md)  
- [RFC-002](RFC-002-design-system.md)  
- [ADR-004](../decisions/ADR-004-design-tokens.md)  
- [ADR-005](../decisions/ADR-005-intent-emit-escape.md)  
- `packages/ourui/ourui/emit/html.py`
