# Node identity

Normative fields for OurIR and analysis nodes:

```text
Node {
  id: NodeId
  kind: NodeKind
  span: SourceSpan
  attributes: Attributes
  metadata: Metadata
  children: [NodeId]
  provenance: Provenance   # ordered transform trail
  revision: Revision
  generation: Generation
  hash: ContentHash
}
```

## Rules

- **I5** — `span` is mandatory.
- **I7** — nodes are immutable; transforms allocate new nodes.
- **provenance** records expansion/lowering history (not a single parent pointer).
- **revision / generation / hash** support incremental compilation later; P0 may set `revision=0`, `generation=0`, and a content hash over canonical payload.
- Graph edges reference `NodeId` values.

## SourceSpan

```text
SourceSpan { path, start_line, start_col, end_line, end_col }
```

Lines are 1-based; columns are 0-based (Python `ast` convention).
