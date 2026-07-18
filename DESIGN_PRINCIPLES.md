# Design Principles

## Technical slogan

> **Developer writes intent. Compiler writes implementation. Host receives primitives.**

This is the engineering philosophy of OurUI, not marketing copy.

## Product focus (now)

**Foundation first:** fill the **utility / style-intent catalog** (Tailwind-depth props → finite `.ourui-*` CSS). Example: `aspect="video"` → `aspect-ratio: 16 / 9`.

| Layer | Role |
|---|---|
| **Style intents** | Craft depth — `aspect=`, `pad_x=`, `width=`, `grow=`, … ([ADR-013](docs/decisions/ADR-013-style-intent-catalog.md)) |
| **`ui.Theme`** | Thin brand sheet — color/type/space roles, optional `density=`, optional `page=` measure. **Not** the utility catalog. |
| **Thin `ui.*` kinds** | Emit mapping (`Page`, `Nav`, `Button`, …) — not a component marketplace |
| **Composed UI** | Out of package for now — compose primitives + utilities in app code later |

See [VISION.md](VISION.md).

## Core principles

### Everything is compiled

Authoring Python is not executed as UI in the browser. It is analyzed and lowered through the OurIR stack into HTML/CSS/JS (and later other hosts).

### Everything is explicit

Names, domains, and stages are named. Hidden framework magic is rejected when it obscures Compilation Flow.

### Everything is deterministic

Given the same source and compiler version, artifacts match. Passes do not depend on ambient nondeterminism.

### Everything is inspectable

Compilers can dump Semantic Graph, Analysis Views, Presentation Graph, Resolved Design, and OurIR stages. Contributors debug with artifacts, not guesswork.

### Host Contract

Web emit requires **RTR + Resolved Design** (RFC-003). Theme roles and **style intents** (utility scales → finite `.ourui-*` classes) flow through resolve and emit — not ad-hoc CSS strings or Tailwind class authoring in Python.

### Utilities are the craft story

Craft depth is the **utility catalog**. Theme roles alone do not “solve craft.” Expanding Stable `ui.*` with composed section patterns is out of scope while the catalog is incomplete ([ADR-014](docs/decisions/ADR-014-language-primitives-vs-kit.md)).

### Everything is traceable

Every node carries `SourceSpan` and **provenance** so expansions and lowerings map back to source.

### Everything is queryable

Analysis Views answer questions such as: *who uses `Theme.primary`?* *who calls this server function?*

## Separation of concerns

| Actor | Writes |
|---|---|
| Developer | Intent (Python props + thin `ui.*` kinds) |
| Compiler | Implementation (graphs, OurIR, emitters, utility CSS) |
| Host | Primitives (DOM, PDF objects, …) |

## Related documents

- Hard rules: [INVARIANTS.md](INVARIANTS.md)
- Structure: [ARCHITECTURE.md](ARCHITECTURE.md)
- Contributor narrative: [COMPILER_BOOK.md](COMPILER_BOOK.md)
- Product north-star: [VISION.md](VISION.md)
- Spec status: [SPEC_STATUS.md](SPEC_STATUS.md)
