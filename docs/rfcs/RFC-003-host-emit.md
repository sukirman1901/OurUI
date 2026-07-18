# RFC-003: Host Contract

**Status:** Draft  
**Depends on:** [RFC-001](RFC-001-presentation-system.md) Accepted; [RFC-002](RFC-002-design-system.md) Accepted  
**Track:** Generation 3 — Host  
**Target release:** `0.3.0` (web host consumes contract; package may stay `ourui` until split)

## Motivation

Generation 1 proved a UI language can compile and run.  
Generation 2 proved presentation meaning can be separated from design knowledge:

```text
Presentation Graph  +  Design System  →  Resolved Design
```

Those artifacts exist in `ourui dump` (schema 12). Emit does **not** consume them yet. The provisional web path is still:

```text
RTR  +  Theme tables  +  _BASE_CSS  →  HTML / CSS / JS
```

That makes the **web emitter** the accidental center of the architecture. Generation 3 must prove the opposite: **Host is a consumer of a stable contract**, and web is only the first host.

## Center of this RFC (locked bias)

**Not** “build a CSS AST first.”

**Yes** — define a **Host Contract**:

```text
Host
  Input:   RTR  +  Resolved Design  (+ optional Layout / runtime metadata)
  Output:  medium-specific product (HTML+CSS+JS today; PDF / native later)
```

CSS AST (if any) is an **implementation detail of the web host**, not the product of the Presentation or Design System layers.

## Generational context

| Generation | Proof | Status |
|------------|-------|--------|
| **1** Language infrastructure | Intent → SG → IIR → LTR → RTR → running app | Done |
| **2** Semantic presentation | PG + DS → Resolved Design (dump) | Done (`0.2.1`) |
| **3** Host | Host consumes `RTR + Resolved Design` via a clean contract | **This RFC** |

## Host Contract — v0 sketch

### Inputs (required)

| Input | Role |
|-------|------|
| **RTR** | Structure, text, events, binds, host kinds / attributes |
| **Resolved Design** | Per-node concrete values (`fill`, `fg`, `radius`, spacing, …) + mode/pack metadata |

### Inputs (optional / later)

| Input | Role |
|-------|------|
| LTR | Layout hints if a host needs them beyond RTR |
| Session / runtime metadata | Prod sessions, HMR — host runtime, not contract core |

### Outputs (web host v0)

| Output | Notes |
|--------|-------|
| HTML | Structure + hooks from RTR; presentation attrs from Resolved Design |
| CSS | Generated from Resolved Design (+ host-private chrome CSS if needed) |
| JS | Events / binds / RPC — still driven by RTR runtime surface |
| Assets | Fonts, icons later — out of v0 spike |

### Non-goals for Contract v0

- Material / Fluent packs  
- Plasma visual parity  
- New chrome (`ui.Nav`)  
- Splitting `ourui-web` as a separate package (may stay in-tree until contract stabilizes)  
- Mandating a CSS AST shape before HTML emit can read Resolved Design  

## Host responsibilities (questions the contract must answer)

1. How does **HTML** attach Resolved Design values to nodes (classes, inline, data attrs, CSS vars)?  
2. How does **JS** continue to read events / binds from RTR without owning design tokens?  
3. How is **CSS** produced from Resolved Design (and what remains host-private chrome)?  
4. How would **PDF** later map the same Resolved Design literals (no CSS required)?  
5. How would **native** later map the same Resolved Design literals?

Web answers (1)–(3) in the first implementation. (4)–(5) constrain the contract so we do not bake CSS-only shapes into Resolved Design (already host-neutral literals per RFC-002).

## Rules

1. Web HTML emitter must **stop owning** design-token tables as the source of truth (`theme.py` / `_BASE_CSS` tone colors become migration debt).  
2. **Resolved Design** remains host-neutral (hex/rem/literals — not `var(--ourui-*)` selectors). Hosts may *emit* CSS variables if they choose.  
3. **Presentation Graph** is not a Host input for emit v0 (Host reads Resolved Design; PG stays compiler/debug).  
4. Dump may gain host-facing emit notes; schema bump only if serialized contract fields change.  
5. Chrome freeze continues until web emit is on the contract path.

## Migration plan (provisional → contract)

| Step | Deliverable |
|------|-------------|
| **A** | Accept Host Contract text (this Draft → Accepted) |
| **B** | Spike: web emit reads `resolved_design` for Button/`tone` colors (leave layout chrome CSS if needed) |
| **C** | Remove emit dependency on `DEFAULT_*` token tables for tones |
| **D** | Document remaining `_BASE_CSS` as host-private chrome only |
| **E** | Release **0.3.0** when web emit path is contract-primary |
| **F** | Optional later: CSS AST module inside web host; package split `ourui-web` |

## Acceptance criteria

- [ ] Host Contract vocabulary frozen: **Host**, **Host Contract**, inputs `RTR` + `Resolved Design`  
- [ ] Explicit: CSS AST is optional web implementation, not Gen-3 gate  
- [ ] Spike plan B–E agreed  
- [ ] No Material / Nav / Plasma in the critical path  

## Implementation checklist (post-Accept)

1. Wire `emit` to take `resolved_design` from pipeline  
2. Tests: Button primary fill/fg from Resolved Design, not Theme table alone  
3. CHANGELOG + SPEC_STATUS (emit provisional → contract-backed)  
4. Roadmap Generation 3 → Done at `0.3.0`

## References

- [RFC-001](RFC-001-presentation-system.md)  
- [RFC-002](RFC-002-design-system.md)  
- [ADR-004](../decisions/ADR-004-design-tokens.md) (provisional tokens)  
- [ADR-005](../decisions/ADR-005-intent-emit-escape.md)  
- [architecture sketch](../architecture/presentation-sketch.md)  
- `packages/ourui/ourui/emit/html.py` (provisional consumer to replace)
