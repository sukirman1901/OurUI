# Analysis Views

Analysis Views are **derived indexes** over the Semantic Graph ([I8](../../INVARIANTS.md)). They are not Compilation Flow stages.

## Interface

Conceptually:

```text
AnalysisView
  name: str
  build(semantic_graph) -> view
```

Passes request capabilities:

```text
Require<DependencyGraph>()
Require<FlowGraph>()
```

## Views (vocabulary)

| View | Purpose |
|---|---|
| DependencyGraph | Impact edges (e.g. theme token usage) |
| CallGraph | Call relationships |
| ThemeGraph | Theme token structure |
| StateGraph | State dependencies |
| ImportGraph | Import relationships |
| FlowGraph | UI action → server → effect → response |

P0 implements **DependencyGraph** minimally.
