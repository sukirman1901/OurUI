# Compiler Book

Contributor guide: **how compilation works**. This is not a normative specification. Normative rules live in [INVARIANTS.md](INVARIANTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), and `spec/`.

Style inspiration: Rustc Dev Guide, LLVM programmer guides.

## 0. Read first

1. [README.md](README.md) — slogan and dump CLI  
2. [INVARIANTS.md](INVARIANTS.md) — hard rules  
3. [ARCHITECTURE.md](ARCHITECTURE.md) — Compilation Architecture  

## 1. Compilation Flow (through `1.9.x`)

```text
Python source
  → Parse (Python AST)
  → Analyze (Semantic Graph + DependencyGraph view)
  → Intent Lowering (IIR)
  → Presentation Graph + Design System → Resolved Design
      (tokens + optional scale overrides from ui.Theme)
  → Layout Lowering (LTR)
  → Render Lowering (RTR / HostNode)
  → Serialize JSON (`ourui dump`, schema 30 additive; 25 Frozen baseline)
  → Emit HTML/CSS/JS (`ourui emit` — RTR + Resolved Design;
      style intent utilities + motion host CSS)
```

Later: routing refinements. LSP ships as `ourui lsp` (completions include style intent values).

## 2. How the parser works (P0)

- Read source text; record path for spans.
- Use Python’s `ast.parse`.
- Walk the AST for assignments and calls that look like UI construction.
- Attach `lineno`/`col_offset` into `SourceSpan`.

See `packages/ourui/ourui/parse/`.

## 3. How the Semantic Graph is built

- Each UI call becomes a graph node with a stable `NodeId`.
- Parent/child nesting becomes edges (`child_of` / `contains`).
- Attribute keys/values are stored on the node.
- Theme-like attribute values create edges to synthetic theme nodes.

The Semantic Graph is the analysis source of truth.

## 4. How Analysis Views work

Views implement a shared contract and are **derived** from the Semantic Graph (I8).

P0 ships **DependencyGraph**: edges such as `uses_theme` from widgets to theme tokens.

Passes should conceptually `Require<DependencyGraph>()` rather than hard-coding traversal forever — plugins will rely on this.

## 5. How Intent Lowering works

Intent Lowering reads the Semantic Graph (+ views) and produces **IIR** nodes in domains:

- Intent Domain — `Page`, `Hero`, `Section`, …
- Presentation Domain — `Button`, `Card`, `Text`, …
- Behavior Domain — reserved for later (events, server)

IIR must not contain host tags (I4).

## 6. How Layout Lowering works

Layout Lowering maps IIR kinds to layout objects (`Column`, `Grid`, `Box`, …), preserves `NodeId` and children, appends `lowering:layout` to provenance, and records `from_intent`. No HTML tags. See `packages/ourui/ourui/lowering/layout.py` and [spec/ir/ltr.md](spec/ir/ltr.md).

## 7. How Render Lowering works

Render Lowering maps LTR objects to **HostNode** kinds (`Container`, `Leaf`, `Text`, …). Textual props become `Text` nodes. Semantic `role` is recorded for emitters — never HTML tags. See `packages/ourui/ourui/lowering/render.py` and [spec/ir/rtr.md](spec/ir/rtr.md).

## 8. Serialization and dump

All artifacts must be serializable (I10). `ourui dump` emits a single JSON document:

```json
{
  "version": 3,
  "semantic_graph": { ... },
  "dependency_graph": { ... },
  "iir": { ... },
  "ltr": { ... },
  "rtr": { ... }
}
```

Deterministic key ordering is required for golden tests (I6).

## 9. Adding an Analysis View (later)

1. Propose via RFC if it introduces new vocabulary.  
2. Implement view builder from Semantic Graph.  
3. Register under Analyze.  
4. Document in COMPILER_BOOK + `spec/ir/analysis-views.md`.  
5. Add dump section + tests.

## 10. How the HTML/JS emitter works

The emitter reads **only** RTR (`HostNode` tree + handlers). It maps `role` → tags and `events.click` → `data-ourui-on-click`, then inlines a small shim (`OurUI.invoke`). See `packages/ourui/ourui/emit/` and [spec/renderer/html.md](spec/renderer/html.md).

## 11. How to run locally

```bash
pip install -e packages/ourui
ourui dump examples/example.py
ourui emit examples/example.py
ourui serve examples/example.py   # http://127.0.0.1:8765/
ourui lsp                         # stdio LSP for editors
pytest tests/p0
```

`serve` recompiles on each GET, executes `@server` handlers on `POST /__ourui/call/<name>`, and pushes HMR reloads over `GET /__ourui/hmr` (SSE) when the source file changes.

## 13. Language Server (Phase L)

`ourui lsp` speaks LSP over stdio (Content-Length framed JSON-RPC). It helps author OurUI Python modules with:

- **Completion** after `ui.` → `Page`, `Hero`, `Section`, `Button`, `Text`, `Card`, `Grid`
- **Completion** for top-level keywords: `State`, `server`, `Component`
- **Hover** one-line docs for `ui.*` components

Editor setup (VS Code / Cursor example — add to workspace or user settings):

```json
{
  "python.languageServer": "None",
  "python.analysis.diagnosticMode": "openFilesOnly"
}
```

Use an LSP client extension or `"ourui.lsp.command": ["ourui", "lsp"]` if your editor supports custom language servers. The server lives in `packages/ourui/ourui/lsp/` and does not require full compiler analysis for completions.

## 12. Changing LOCKED architecture

See [RFC_PROCESS.md](RFC_PROCESS.md). Opinions without implementation evidence are rejected.
