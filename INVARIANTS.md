# Invariants

These rules **must not be violated**. Principles explain philosophy; invariants forbid breakage. Changing an invariant requires an [RFC](RFC_PROCESS.md).

## Invariants

| ID | Rule |
|---|---|
| **I1** | Python AST never reaches emitters. |
| **I2** | Emitters only consume RTR (via **HostNode**). |
| **I3** | RTR contains no language (Python) semantics. |
| **I4** | IIR contains no host semantics (no HTML tags). |
| **I5** | Every Node has a `SourceSpan`. |
| **I6** | Every compilation phase is deterministic. |
| **I7** | The compiler never mutates a previous artifact; passes produce new artifacts. |
| **I8** | Analysis Views are derived indexes — not Compilation Flow stages. |
| **I9** | Public docs name phases; pass numbers are implementation detail only. |
| **I10** | Every artifact is serializable (cache, LSP, debugger, AI, distributed compile). |

## LOCKED decisions

Do **not** change the following without an accepted RFC backed by implementation evidence that the current design failed:

- Python as the authoring language
- Semantic Graph as the source of analysis
- Analysis Views are not Compilation Flow stages
- OurIR as the **IR Stack** (IIR → LTR → RTR)
- Emitters only consume RTR / HostNode
- Nodes are immutable
- `SourceSpan` is mandatory on node identity
- Core Documents are separate from detailed specs and ADRs
- Compilation Flow: **Parse → Analyze → Lower → Optimize → Emit**

## Vocabulary freeze

Official vocabulary (new terms require an RFC):

**Semantic Graph** · **Analysis View** · **IIR** · **LTR** · **RTR** · **HostNode** · **Provenance** · **Emitters** · **OurIR** (IR Stack) · **Compilation Flow** · **Compilation Architecture** · **Intent Domain** · **Behavior Domain** · **Presentation Domain**

## Naming note

- **Compilation Architecture** — document / chapter title ([ARCHITECTURE.md](ARCHITECTURE.md)).
- **Compilation Flow** — the diagram and phase sequence.
