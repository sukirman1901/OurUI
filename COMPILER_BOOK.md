# Compiler Book

Contributor guide: **how compilation works**. This is not a normative specification. Normative rules live in [INVARIANTS.md](INVARIANTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), and `spec/`.

Style inspiration: Rustc Dev Guide, LLVM programmer guides.

## 0. Read first

1. [README.md](README.md) — slogan and dump CLI  
2. [INVARIANTS.md](INVARIANTS.md) — hard rules  
3. [ARCHITECTURE.md](ARCHITECTURE.md) — Compilation Architecture  

## 1. Compilation Flow (through Phase E)

```text
Python source
  → Parse (Python AST)
  → Analyze (Semantic Graph + DependencyGraph view)
  → Intent Lowering (IIR)
  → Layout Lowering (LTR)
  → Render Lowering (RTR / HostNode)
  → Serialize JSON (`ourui dump`)
  → Emit HTML/CSS (`ourui emit`)
```

Later: JS emit, runtime, HMR, LSP.

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

## 10. How the HTML emitter works

The emitter reads **only** RTR (`HostNode` tree). It maps `role` → tags (`button`, `main`, `header`, …) and layout → CSS classes. See `packages/ourui/ourui/emit/html.py` and [spec/renderer/html.md](spec/renderer/html.md).

## 11. How to run locally

```bash
pip install -e packages/ourui
ourui dump examples/example.py
ourui emit examples/example.py
pytest tests/p0
```

## 12. Changing LOCKED architecture

See [RFC_PROCESS.md](RFC_PROCESS.md). Opinions without implementation evidence are rejected.
