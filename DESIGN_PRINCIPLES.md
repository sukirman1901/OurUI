# Design Principles

## Technical slogan

> **Developer writes intent. Compiler writes implementation. Host receives primitives.**

This is the engineering philosophy of OurUI, not marketing copy.

## Core principles

### Everything is compiled

Authoring Python is not executed as UI in the browser. It is analyzed and lowered through the OurIR stack.

### Everything is explicit

Names, domains, and stages are named. Hidden framework magic is rejected when it obscures Compilation Flow.

### Everything is deterministic

Given the same source and compiler version, artifacts match. Passes do not depend on ambient nondeterminism.

### Everything is inspectable

Compilers can dump Semantic Graph, Analysis Views, and OurIR stages. Contributors debug with artifacts, not guesswork.

### Everything is traceable

Every node carries `SourceSpan` and **provenance** so expansions and lowerings map back to source.

### Everything is queryable

Analysis Views answer questions such as: *who uses `Theme.primary`?* *who calls this server function?*

## Separation of concerns

| Actor | Writes |
|---|---|
| Developer | Intent (Python DSL) |
| Compiler | Implementation (graphs, OurIR, emitters) |
| Host | Primitives (DOM, PDF objects, …) |

## Related documents

- Hard rules: [INVARIANTS.md](INVARIANTS.md)
- Structure: [ARCHITECTURE.md](ARCHITECTURE.md)
- Contributor narrative: [COMPILER_BOOK.md](COMPILER_BOOK.md)
