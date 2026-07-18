# ADR-009: Structured diagnostics and Derived (Phase V)

**Status:** Accepted + Implemented (diagnostics Stable; Derived Draft)  
**Date:** 2026-07-18  

## Context

Compile failures surfaced as raw tracebacks. Authors and LSP needed path + span. Computed values needed a Draft path without inventing client stores.

## Decision

1. **Diagnostics** — analyzer/pipeline emit `{code, message, path, start_line, end_line, …}`; `ourui check` prints them; LSP publishes `textDocument/publishDiagnostics`.  
2. **Derived** — `Derived(expr)` module-level companion to `State`; read-only; deps inferred from Name refs in the callable/lambda body when possible; Draft until a follow-up ADR promotes Stable.

## Consequences

Dump may include `derived` map. `ourui check` exits non-zero on errors. Derived does not accept client writes.
